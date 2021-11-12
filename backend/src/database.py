# This script contains all methods that operates database

from macros import Macros
from utils import Utils

import os

class Database:

    @classmethod
    def user_exists_in_db(cls, cursor, mysql, hash_username, hash_password=None):
        
        if not hash_password:
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (hash_username, hash_password))
        else:
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (hash_username,))
        # end if
        account = cursor.fetchone()
        if account:
            return account
        # end if
        return

    @classmethod
    def insert_account_record(cls, cursor, mysql, data):
        # query = "INSERT INTO `accounts` (`username`, `password`, `email`) VALUES ('test_username', 'test_pw', 'test@test.com');"
        # data: [hash_username, hash_password, email]
        cursor.execute(
            'INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)',
            (data[0], data[1], data[2])
        )
        mysql.connection.commit()
        return cursor, mysql

    @classmethod
    def delete_account_record(cls, cursor, mysql, data):
        pass
    
    @classmethod
    def update_account_record(cls, cursor, mysql, data):
        pass

    
