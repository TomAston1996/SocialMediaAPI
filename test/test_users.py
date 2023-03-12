from fastapi.testclient import TestClient
from app.main import app

# Pytest command: pytest -v -s --disable-warnings in root folder

client = TestClient(app)

def test_root(): 
    res = client.get('/')
    assert res.json().get('message') == 'root'
    assert res.status_code == 200