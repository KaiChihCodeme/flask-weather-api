from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from exceptions import KeyNotExistException
from flask import current_app as app

Base = declarative_base()
db = SQLAlchemy(model_class=Base)

class weather(Base):
    __tablename__ = 'weather'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    temperature = Column(Numeric(5,2), nullable=False)  # Numeric may accept string like "40.6"
    humidity = Column(Numeric(5,2), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
def db_add_weather(city, temperature, humidity, description):
    try:
        new_weather = weather(city=city, temperature=temperature, humidity=humidity, description=description)
        db.session.add(new_weather)
        db.session.commit()
        return new_weather
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error in adding weather to db: {e}")
        return None

def db_get_all_weathers():
    return weather.query.all()

def db_get_all_weathers_paging(page, limit):
    return weather.query.paginate(page=page, per_page=limit, error_out=False)

def db_get_weather(id):
    return weather.query.get(id)

def db_update_weather(id, **kwargs):
    try:
        w = weather.query.get(id)
        if w:
            for key, value in kwargs.items():
                if hasattr(w, key):
                    setattr(w, key, value)
                else:
                    app.logger.error(f"Invalid key in update weather: {key}")
                    return KeyNotExistException(key)
            db.session.commit()
            return w
        return None
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error in updating weather in db: {e}")
        return e

def db_delete_weather(id):
    w = weather.query.get(id)
    if w:
        db.session.delete(w)
        db.session.commit()
        return True
    app.logger.info(f"Delete weather with id {id} not found")
    return False