from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, LazyString, LazyJSONEncoder
from db import db
from config import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER, DATABASE_NAME
from weather import weather_bp
from cache import redis
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    isTesting = False
    
    if test_config is not None:
        app.config.update(test_config)
        isTesting = True
        
    configure_logger(app)
    configure_extensions(app, isTesting)
    configure_apispec(app)
    configure_blueprints(app)
    
    # Add health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    @app.errorhandler(404)
    def page_not_found(e):
        return {'message': 'Resource not found'}, 404
    
    return app

def configure_extensions(app, isTesting=False, test_redis=None):
    # initialize all used extensions
    # intialize db
    if not isTesting:
        conn_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}'
        app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
    db.init_app(app)
    
    # initialize redis
    redis.init_redis(isTesting)
    try:
        redis.ping()
        app.logger.info("Connected to redis")
    except Exception as e:
        app.logger.error(f"Error connecting to redis: {e}")
    
def configure_apispec(app):
    # configure swagger for api spec
    app.json_encoder = LazyJSONEncoder
    template = dict(
        swagger='2.0',
        info=dict(
            title='weather API',
            description='A simple weather API',
            version='1.0'
        )
    )
    swagger = Swagger(app, template=template)
    
def configure_blueprints(app):
    app.register_blueprint(weather_bp)
    
def configure_logger(app):
    handler = RotatingFileHandler('weather.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    
    # Add a formatter to include the timestamp in logs
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)