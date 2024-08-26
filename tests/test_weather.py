import pytest
from app import create_app, db
from exceptions import KeyNotExistException
import fakeredis

from sqlalchemy_utils import database_exists, create_database, drop_database

@pytest.fixture(scope='module')
def test_app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_database.db'})
    with app.test_client() as testing_client:
        with app.app_context():
            if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()
            if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
                drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

@pytest.fixture
def client(test_app):
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_database.db'})
    with app.test_client() as client:
        yield client

    """
    POST /weather/
    """
def test_create_weather(client):
    sample_weather = {
        "city": "New York",
        "temperature": 20.5,
        "humidity": 50.5,
        "description": "Cloudy"
    }
    response = client.post('/weather/', json=sample_weather)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['message'] == "weather successfully created!"
    assert 'weather' in data
    
def test_create_weather_missing_field(client):
    sample_weather = {
        "city": "New York",
        "temperature": 20.5,
        "description": "Cloudy"
    }
    response = client.post('/weather/', json=sample_weather)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['message'] == "weather creation failed!"
    
    """
    GET /weathers/
    """
def test_get_all_weathers(client):
    response = client.get('/weather/')
    data = response.get_json()
    
    assert response.status_code == 200
    assert 'weathers' in data
    
    """
    GET /weathers/<int:page>/<int:limit>
    """
def test_get_all_weathers_paging(client):
    response = client.get('/weather/1/5')
    data = response.get_json()
    
    assert response.status_code == 200
    assert 'weathers' in data
    assert 'total' in data
    assert 'pages' in data
    assert 'page' in data
    
    """
    GET /weathers/<int:id>
    """
def test_get_weather(client):
    response = client.get('/weather/1')
    data = response.get_json()
    
    assert response.status_code == 200
    assert 'weather' in data
    
def test_get_weather_not_found(client):
    response = client.get('/weather/100')
    data = response.get_json()
    
    assert response.status_code == 404
    assert data['message'] == "No weather Found in id: 100"
    
    """
    PATCH /weathers/<int:id>
    """
def test_update_weather(client):
    sample_weather = {
        "city": "New York Updated",
        "temperature": 25.5,
        "humidity": 60.5,
        "description": "Sunny"
    }
    response = client.patch('/weather/1', json=sample_weather)
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['message'] == "weather successfully updated!"
    assert 'weather' in data
    
def test_update_weather_not_found(client):
    sample_weather = {
        "city": "New York Updated",
        "temperature": 25.5,
        "humidity": 60.5,
        "description": "Sunny"
    }
    response = client.patch('/weather/100', json=sample_weather)
    data = response.get_json()
    
    assert response.status_code == 404
    assert data['message'] == "weather id: 100 not found!"
    
def test_update_weather_wrong_field(client):
    sample_weather = {
        "in": "New York Updated",
        "temperature": 25.5,
        "humidity": 60.5,
        "description": "Sunny"
    }
    response = client.patch('/weather/1', json=sample_weather)
    data = response.get_json()
    assert response.status_code == 400
    assert str(data) == "{'message': 'Invalid key: in'}"
    
    """
    DELETE /weathers/<int:id>
    """
def test_delete_weather(client):
    response = client.delete('/weather/1')
    data = response.get_json()
    
    assert response.status_code == 200
    assert data['message'] == "weather successfully removed!"
    
def test_delete_weather_not_found(client):
    response = client.delete('/weather/100')
    data = response.get_json()
    
    assert response.status_code == 404
    assert data['message'] == "No weather Found"