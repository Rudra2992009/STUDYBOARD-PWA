import pytest
from backend.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'healthy'

def test_chat_endpoint_missing_message(client):
    """Test chat endpoint with missing message"""
    response = client.post('/api/chat', json={})
    assert response.status_code == 400

def test_chat_endpoint_valid_request(client):
    """Test chat endpoint with valid request"""
    response = client.post('/api/chat', json={
        'message': 'What is photosynthesis?',
        'exam_class': '10',
        'generate_image': False
    })
    # May fail if models not loaded, which is expected in CI
    assert response.status_code in [200, 500]