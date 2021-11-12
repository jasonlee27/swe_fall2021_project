# This script is to generate test cases using pytest
# the test is run by "python -m pytest"
# at the backend/src

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


# Barcode test cases:
# 12-digit numbers that are uniquely assigned to
# each trade item (Universal Product Code)
@pytest.fixture(scope='module')
def valid_barcode():
    barcode_num = "036000291452"
    return barcode_num

@pytest.fixture(scope='module')
def invalid_barcode():
    barcode_num = "ol2345b789oo"
    return barcode_num
