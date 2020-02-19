from json import JSONDecodeError
import rest_api
import pytest
import json
from jsonschema import validate, ValidationError

API_URL = '/api/Albums'


def test_app():
    app = rest_api.app
    client = app.test_client()
    res = client.get(API_URL)
    assert res.status_code == 200


@pytest.fixture
def app():
    _app = rest_api.app
    return _app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


def test_app_runs(client):
    res = client.get(API_URL)
    assert res.status_code == 200


def test_app_returns_json(client):
    res = client.get(API_URL)
    assert res.headers['Content-Type'] == 'application/json'


def test_app_data(client):
    res = client.get(API_URL)
    data = json.loads(res.data)
    assert type(data) == dict
    assert 'records' in data
    assert type(data['records']) == list


def test_app_methods(client):
    app = rest_api.app
    client = app.test_client()
    # POST
    res = client.post(API_URL, json={'Album': 'Test'})
    data = json.loads(res.data)
    id_ = data['id']
    assert {'Album': 'Test'} == data['fields']
    # PATCH
    res = client.patch(API_URL, json={'id': id_, 'Album': 'renamed'})
    data = json.loads(res.data)
    id_ = data['id']
    assert {'Album': 'renamed'} == data['fields']
    # DELETE
    res = client.delete(API_URL, json={'id': id_})
    data = json.loads(res.data)
    assert 'deleted' in data
    # WRONG POST
    res = client.post(API_URL, json={'Album': 100})
    assert res.status_code == 400
