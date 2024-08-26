import os
from dotenv import load_dotenv

ENV = os.getenv('FLASK_ENV', 'dev')
DEBUG = ENV == 'dev'

# Load environment variables from .env file
# dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
# load_dotenv(dotenv_path=dotenv_path)

# DB
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'weather')

# redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)