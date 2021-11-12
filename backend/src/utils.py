import hashlib
import re, os

from macros import Macros


class Utils:

    @classmethod
    def hashing(cls, input_str, salt="5gz"):
        _input_str = input_str+salt
        h = hashlib.md5(_input_str.encode())
        return h.hexdigest()

    @classmethod
    def isvalid_email(cls, email):
        m = re.match(r'[^@]+@[^@]+\.[^@]+', email)
        return True if m else False

    @classmethod
    def isvalid_username(cls, username):
        m = re.match("^[a-zA-Z0-9_.-]+$", username)
        return True if m else False

    @classmethod
    def isvalid_password(cls, password):
        if len(password)<10:
            return False
        # end if
        m = re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{10,100}$", password)
        return True if m else False
    
    @classmethod
    def isvalid_barcode(cls, barcode):
        m = re.match(r"^[0-9]+$", barcode)
        return True if m else False

    
