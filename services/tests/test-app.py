# Create tests for flask-app.py
import pytest
from flask_app import create_app


def test_app():
    app = create_app()
    assert app is not None


def test_app_config():
    app = create_app()
    assert app.config['SECRET_KEY']


def test_app_config_test():
    app = create_app()
    assert app.config['TESTING'] is False


if __name__ == '__main__':
    pytest.main()