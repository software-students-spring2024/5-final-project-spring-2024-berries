
import pytest
from web_app.app import app as flask_app  
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
import bcrypt

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/test_database"
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def mock_mongo_client(monkeypatch):
    class FakeMongoClient:
        def __init__(self, uri):
            pass
        
        def __getitem__(self, name):
            return FakeDatabase()

    class FakeDatabase:
        def __getitem__(self, name):
            return FakeCollection()
    
    class FakeCollection:
        def find_one(self, query):
            if query.get("username") == "johndoe":
                return {"username": "johndoe", "password": "hashed_password"} 
            return None
        
        def insert_one(self, user):
            return
    
    monkeypatch.setattr(MongoClient, '__init__', FakeMongoClient.__init__)
    monkeypatch.setattr(MongoClient, '__getitem__', FakeMongoClient.__getitem__)

def test_register_new_user(client, mocker):
    mocker.patch('bcrypt.hashpw', return_value=b'hashed_password')  
    response = client.post('/register', data={
        'name': 'John Doe',
        'username': 'newuser',
        'password': 'securepassword'
    })
    assert response.status_code == 200  

def test_register_existing_user(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value={'username': 'johndoe'})
    response = client.post('/register', data={
        'name': 'John Doe',
        'username': 'johndoe',
        'password': 'securepassword'
    })
    assert response.status_code == 200

def test_login_success(client, mocker):
    mocker.patch('bcrypt.checkpw', return_value=True)
    mocker.patch('pymongo.collection.Collection.find_one', return_value={'username': 'johndoe', 'password': 'hashed_password'})
    response = client.post('/login', data={'username': 'johndoe', 'password': 'securepassword'})
    assert response.status_code == 404

def test_login_failure(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value=None)
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'})
    assert response.status_code == 404

def test_logout(client):
    with client:
        client.post('/login', data={'username': 'johndoe', 'password': 'securepassword'})
        client.get('/logout')
        response = client.get('/home')
        assert response.status_code == 302 

def test_find_coffee_shops(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"cafes": [{"name": "Best Coffee", "location": "Downtown"}]}
        response = client.post("/find_coffee_shops", json={"latitude": 40.7128, "longitude": -74.0060})
        assert response.status_code == 200
        assert "Best Coffee" in response.data.decode()

def test_home_access_when_logged_in(client, mocker):
    with client.session_transaction() as sess:
        sess['username'] = 'johndoe'
    response = client.get('/home')
    assert response.status_code == 200

def test_get_login_page(client):
    response = client.get('/')
    assert response.status_code == 200 

def test_get_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_get_home_page(client):
    response = client.get('/home')
    assert response.status_code == 302

def test_get_coffee_page(client):
    response = client.get('/find_coffee_shops')
    assert response.status_code == 405 
   
def test_login_incorrect_password(client, mocker):
    mocker.patch('pymongo.collection.Collection.find_one', return_value={'username': 'johndoe', 'password': bcrypt.hashpw('real_password'.encode('utf-8'), bcrypt.gensalt())})
    mocker.patch('bcrypt.checkpw', return_value=False)
    response = client.post('/', data={'username': 'johndoe', 'password': 'wrong_password'})
    assert response.status_code == 200 

