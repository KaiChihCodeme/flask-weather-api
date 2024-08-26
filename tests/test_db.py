from db import db,db_add_weather, db_get_all_weathers, db_get_all_weathers_paging, db_get_weather, db_update_weather, db_delete_weather, weather
from app import create_app
from exceptions import KeyNotExistException
from datetime import datetime
import pytest

@pytest.fixture
def test_client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    }) 
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()  
            yield testing_client  
            db.session.remove()
            db.drop_all() 

    """
    Test cases for db_add_weather function
    """
def test_db_add_weather_success(test_client):
    # Test case 1: Adding a new weather
    city = "New York" 
    temperature = 20.5
    humidity = 50.5
    description = "Cloudy"

    new_weather = db_add_weather(city, temperature, humidity, description)

    assert new_weather is not None
    assert new_weather.city == city
    assert new_weather.temperature == temperature
    assert new_weather.humidity == humidity
    assert new_weather.description == description

def test_db_add_weather_missing_fields(test_client):
    # Test case 2: Adding a weather with missing required fields
    city = "New York" 
    temperature = 20.5
    humidity = 50.5 

    with pytest.raises(TypeError) as excinfo:
        new_weather = db_add_weather(city, temperature, humidity)  # Missing 'description' parameter

    assert "missing 1 required positional argument: 'description'" in str(excinfo.value)

def test_db_add_weather_invalid_temperature(test_client):
    # Test case 3: Adding a weather with invalid temperature
    city = "New York" 
    temperature = "Queen"
    humidity = 50.5
    description = "Cloudy"

    new_weather = db_add_weather(city, temperature, humidity, description)

    assert new_weather is None
    
    """
    Test cases for db_get_all_weathers function
    """
def test_db_get_all_weathers(test_client):
    # Test case: Getting all weathers after adding some weathers
    db_add_weather("New York", 20.5, 50.5, "Cloudy")
    db_add_weather("Tokyo", 25.5, 60.5, "Sunny")
    db_add_weather("London", 15.5, 40.5, "Rainy")
    weathers = db_get_all_weathers()
    assert len(weathers) == 3
    
    """
    Test cases for db_get_all_weathers_paging function
    """
def test_db_get_all_weathers_paging(test_client):
    # Test case: Getting all weathers with pagination
    db_add_weather("New York", 20.5, 50.5, "Cloudy")
    db_add_weather("Tokyo", 25.5, 60.5, "Sunny")
    db_add_weather("London", 15.5, 40.5, "Rainy")
    paginated_weathers = db_get_all_weathers_paging(1, 2)
    assert paginated_weathers.total == 3
    assert paginated_weathers.pages == 2
    assert len(paginated_weathers.items) == 2
    
    """
    Test cases for db_get_weather function
    """
def test_db_get_weather(test_client):
    # Test case: Getting a weather by id
    weather = db_add_weather("New York", 20.5, 50.5, "Cloudy")
    weather_id = weather.id
    retrieved_weather = db_get_weather(weather_id)
    assert retrieved_weather is not None
    assert retrieved_weather.id == weather_id
    
def test_db_get_weather_invalid_id(test_client):
    # Test case: Getting a weather with invalid id
    retrieved_weather = db_get_weather(100)
    assert retrieved_weather is None
    
    """
    Test cases for db_update_weather function
    """
def test_db_update_weather(test_client):
    # Test case: Updating a weather with valid fields
    weather = db_add_weather("New York", 20.5, 50.5, "Cloudy")
    weather_id = weather.id
    updated_weather = db_update_weather(weather_id, city="Tokyo", temperature=25.5, humidity=60.5, description="Sunny")
    assert updated_weather is not None
    assert updated_weather.city == "Tokyo"
    assert updated_weather.temperature == 25.5
    assert updated_weather.humidity == 60.5
    assert updated_weather.description == "Sunny"
    
def test_db_update_weather_invalid_key(test_client):
    # Test case: Updating a weather with invalid key
    weather = db_add_weather("New York", 20.5, 50.5, "Cloudy")
    weather_id = weather.id

    updated_weather = db_update_weather(weather_id, city="Tokyo", temperature=25.5, humidity=60.5, description="Sunny", rainfall=0)  # Invalid key 'rainfall'
    assert isinstance(updated_weather, KeyNotExistException), "Expected result to be an instance of KeyNotExistException"
    assert str(updated_weather) == "Invalid key: rainfall", "Expected exception message to match 'Invalid key: rainfall'"
    
def test_db_update_weather_invalid_id(test_client):
    # Test case: Updating a weather with invalid id
    updated_weather = db_update_weather(100, city="Tokyo", temperature=25.5, humidity=60.5, description="Sunny") 
    assert updated_weather is None
    
    """
    Test cases for db_delete_weather function
    """
def test_db_delete_weather(test_client):
    # Test case: Deleting a weather by id
    weather = db_add_weather("New York", 20.5, 50.5, "Cloudy")
    weather_id = weather.id
    deleted = db_delete_weather(weather_id)
    assert deleted is True
    
def test_db_delete_weather_invalid_id(test_client):
    # Test case: Deleting a weather with invalid id
    deleted = db_delete_weather(100)
    assert deleted is False
    
def test_db_delete_weather_already_deleted(test_client):
    # Test case: Deleting a weather that has already been deleted
    weather = db_add_weather("New York", 20.5, 50.5, "Cloudy")
    weather_id = weather.id
    deleted = db_delete_weather(weather_id)
    assert deleted is True
    deleted = db_delete_weather(weather_id)
    assert deleted is False

    """
    db model to_dict method test
    """
def test_weather_to_dict():
    # Setup: Create a weather instance with known values
    created_at = datetime.now()
    updated_at = datetime.now()
    w = weather(id=1, city="New York", temperature=20.5, humidity=50.5, description="Cloudy", created_at=created_at, updated_at=updated_at)
    
    # Expected dictionary based on the known values
    expected_dict = {
        'id': 1,
        'city': "New York",
        'temperature': 20.5,
        'humidity': 50.5,
        'description': "Cloudy",
        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Execution: Call the to_dict method
    result_dict = w.to_dict()
    
    # Assertion: Compare the returned dictionary to the expected dictionary
    assert result_dict == expected_dict, "The to_dict method returned an unexpected dictionary."