

import pytest

from utils import Utils


# generate test cases for validating
# (username, password, email)
@pytest.fixture(scope='module')
def valid_user():
    user = {
        "username": "leej941",
        "password": "Password2021!@",
        "email": "jxl115330@abc.com"
    }
    return user

@pytest.fixture(scope='module')
def invalid_username_user():
    user = {
        "username": "leej941!",
        "password": "Password2021!@",
        "email": "jxl115330@abc.com"
    }
    return user

@pytest.fixture(scope='module')
def invalid_email_user():
    user = {
        "username": "leej941",
        "password": "Password2021!@",
        "email": "jxl115330abc.com"
    }
    return user

@pytest.fixture(scope='module')
def invalid_password_user():
    user = {
        "username": "leej941",
        "password": "Password!@",
        "email": "jxl115330@abc.com"
    }
    return user
