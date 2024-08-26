import pytest
from sqlalchemy import text
from app import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        from db import db
        db.create_all()
        yield db
        db.drop_all()

def test_db_connection(init_db):
    # Attempt to use the database, e.g., by creating a new model instance or querying
    assert init_db.session.query(text('1')).first() == (1,)  # Simple query to test connection
    