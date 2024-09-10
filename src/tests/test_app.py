from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_goal(client):
    response = client.post(
        '/goal',
        json={'title': 'Ir para academia', 'desired_weekly_frequency': 5},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Ir para academia',
        'desired_weekly_frequency': 5,
    }
