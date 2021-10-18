from app import app
import json
import unittest

test_app = app.test_client()


def test_create_happy_path():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test',
                                'email': 'nice'
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 200
    assert response.is_json
    assert 'id' in response.json


def test_create_no_contact():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test',
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json


def test_create_incorrect_data_type():
    response = test_app.put('/supplier',
                            data=json.dumps({
                                'name': 177013,
                            }), content_type='application/json')
    assert response is not None
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json

def test_delete_non_empty_database():
    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test1',
                                'email': 'nice2'
                            }), content_type='application/json')

    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test2',
                                'email': 'nice2'
                            }), content_type='application/json')

    response1 = test_app.delete("/supplier/1")
    assert response1 is not None
    assert response1.status_code == 200
    
    response2 = test_app.detete("/supplier/1")
    assert response2 is not None
    assert response2.status_code == 200

def test_delete_empty_database():
    response = test_app.delete("/supplier/1")
    assert response is not None
    assert response.status_code == 400
    assert response.is_json
    assert 'error' in response.json

def test_list_all_non_empty_database():
    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test1',
                                'email': 'nice2'
                            }), content_type='application/json')

    test_app.put('/supplier',
                            data=json.dumps({
                                'name': 'test2',
                                'email': 'nice2'
                            }), content_type='application/json')

    response = test_app.get("/suppliers)")
    assert response is not None
    assert response.status_code == 200
    
def test_list_all_empty_database():
    response = test_app.get("/suppliers)")
    assert response is not None
    assert response.status_code == 200

    


