import pytest
from app import app # Importeer je Flask app instantie

@pytest.fixture
def client():
    # Configureer de Flask app voor testen
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """
    Test dat de /api/health route een 200 OK respons geeft
    en dat de JSON status 'ok' is.
    """
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_hello_api(client):
    """
    Test dat de /api route een 200 OK respons geeft
    en de verwachte tekst retourneert.
    """
    response = client.get('/api')
    assert response.status_code == 200
    # Controleer of de respons 'Hello from API!' bevat
    # Let op: de hostname zal variëren in de testomgeving, dus test alleen op het vaste deel.
    assert b'Hello from API!' in response.data
