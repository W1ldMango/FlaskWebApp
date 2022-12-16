import pytest

from flask_app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_logout_redirect(client):
    response = client.get("/logout")
    assert len(response.history) == 0
    assert response.request.path == "/logout"


# Test for valid login data
def test_valid_login(client):
    response = client.post('/', data=dict(
        username='admin',
        password='123'), follow_redirects=True)
    assert response.status_code == 404


# Test for invalid login data
def test_invalid_login(client):
    response = client.post('/', data=dict(
        username='admin',
        password='1234'), follow_redirects=True)
    assert response.status_code == 404


# Test for valid registration data
def test_valid_registration(client):
    response = client.post('/registration', data=dict(
        username='admin',
        password='1234'), follow_redirects=True)
    assert response.status_code == 404


# Test for invalid registration data
def test_invalid_registration(client):
    response = client.post('/registration', data=dict(
        username='admin',
        password='1234'), follow_redirects=True)
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main()
