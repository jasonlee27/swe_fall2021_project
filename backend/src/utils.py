import hashlib
import re, os


class Utils:

    @classmethod
    def hashing(cls, input_str, salt="5gz"):
        _input_str = input_str+salt
        h = hashlib.md5(_input_str.encode())
        return h.hexdigest()

    @classmethod
    def isvalid_email(cls, email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', email)

    @classmethod
    def isvalid_username(cls, username):
        return re.match("^[a-zA-Z0-9_.-]+$", username)

    @classmethod
    def isvalid_password(cls, password):
        if len(password)<10:
            return False
        # end if
        return re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", password)

    
