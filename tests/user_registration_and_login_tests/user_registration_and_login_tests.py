import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_valid_data(client: APIClient) -> None:
    payload = dict(
        username="testuser",
        email="test@email.com",
        password="testpassword",
        title="title",
    )

    response = client.post('/api/register', payload)
    data = response.data["user"]
    assert response.status_code == 201
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_register_invalid_data(client: APIClient) -> None:
    payload = dict(
        username="testuser",
        email="test@email.com",
        password="testpassword",
        title="title"
    )

    client.post('/api/register', payload)
    response = client.post('/api/register', payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_valid_data(client: APIClient) -> None:
    payload = dict(
        username="testuser",
        email="test@email.com",
        password="testpassword",
        title="title"
    )

    client.post('/api/register', payload)
    payload = dict(
        username="testuser",
        password="testpassword"
    )
    response = client.post('/api/login', payload)
    assert response.status_code == 200
    assert "token" in response.data


@pytest.mark.django_db
def test_login_invalid_data(client: APIClient) -> None:
    payload = dict(
        username="testuser",
        password="testpassword"
    )
    response = client.post('/api/login', payload)
    assert response.status_code == 400
    assert "token" not in response.data
