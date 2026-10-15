from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_stats_shape():
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert {'jobs', 'companies', 'sources', 'runs'} <= response.json().keys()

def test_jobs_response_is_paginated():
    response = client.get('/api/jobs?limit=2&sort=newest')
    assert response.status_code == 200
    body = response.json()
    assert {'items', 'total', 'limit', 'offset', 'has_more'} <= body.keys()
    assert len(body['items']) <= 2
