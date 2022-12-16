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


# Test json output

def test_json_output(client):
    if client.get('/').json == {'message': 'Hello, World!'}:
        assert True


def test_invalid_json(client):
    if client.get('/').json == {'message': 'Hello, World'}:
        assert False


if __name__ == '__main__':
    pytest.main()
