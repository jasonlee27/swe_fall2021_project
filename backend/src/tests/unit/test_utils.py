# test utils.py

from utils import Utils


def test_valid_user(valid_user):
    assert Utils.isvalid_username(valid_user["username"])
    assert Utils.isvalid_password(valid_user["password"])
    assert Utils.isvalid_email(valid_user["email"])

def test_invalid_username_user(invalid_username_user):
    assert not Utils.isvalid_username(invalid_username_user["username"])
    
def test_invalid_email_user(invalid_email_user):
    assert not Utils.isvalid_email(invalid_email_user["email"])
    
def test_invalid_password_user(invalid_password_user):
    assert not Utils.isvalid_password(invalid_password_user["password"])
