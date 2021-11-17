# This script contains all methods that operates database

from macros import Macros
from utils import Utils

import os

class Database:

    @classmethod
    def user_exists_in_db(cls, cursor, mysql, hash_username, hash_password=None):
        
        if not hash_password:
            cursor.execute('SELECT * FROM Accounts WHERE username = %s AND password = %s', (hash_username, hash_password))
        else:
            cursor.execute('SELECT * FROM Accounts WHERE username = %s', (hash_username,))
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
            'INSERT INTO Accounts (username, password, email) VALUES (%s, %s, %s)',
            (data[0], data[1], data[2])
        )
        mysql.connection.commit()
        return cursor, mysql

    @classmethod
    def update_password_record(cls, cursor, mysql, data):
        # query = "INSERT INTO `accounts` (`username`, `password`, `email`) VALUES ('test_username', 'test_pw', 'test@test.com');"
        # data: [hash_username, new_hash_password]
        hash_username, new_hash_password, email = data[0], data[1], data[2]
        cursor.execute(
            'UPDATE Accounts SET password = %s WHERE username = %s AND email = %s',
            (new_hash_password, hash_username, email)
        )
        mysql.connection.commit()
        msg = 'Successfully password updated'
        return cursor, mysql, msg

    @classmethod
    def get_stores_exist_in_db(cls, cursor, mysql, location):
        city, state = location[0], location[1]
        cursor.execute('SELECT * FROM Stores WHERE city = %s AND state = %s', (city, state))
        stores = cursor.fetchall()
        if stores:
            return stores
        # end if
        return

    @classmethod
    def add_item_in_db(cls, cursor, mysql, data):
        itemname, quantity = data[0], data[1]
        store_add, store_city, store_state = data[2], data[3], data[4]

        # check if the input item is avaialble in db
        cursor.execute(
            'SELECT * FROM Items I, Stores S 
             WHERE I.location = %s AND I.itemname = %s AND I.quantity >= %s 
             AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s',
            (store_loc, itemname, quantity, state_add, state_city, state_state)
        )
        item_avail = cursor.fetchone()
        if item_avail:
            item_id = item_avail[0]
            cursor.execute(
                'UPDATE Items SET quantity = quantity - %s WHERE id = %d', (quantity, item_id)
            )
            mysql.connection.commit()
            msg = "Successfully item added"
        else:
            msg = "Item selected is not available"
        # end if
        return cursor, mysql, msg

    @classmethod
    def update_item_in_db(cls, cursor, mysql, data):
        itemname, old_quantity, new_quantity = data[0], data[1], data[2]
        store_add, store_city, store_state = data[3], data[4], data[5]

        # check if the input item is avaialble in db
        cursor.execute(
            'SELECT * FROM Items I, Stores S 
             WHERE I.location = %s AND I.itemname = %s AND I.quantity >= 0
             AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s',
            (store_loc, itemname, quantity, state_add, state_city, state_state)
        )
        item_avail = cursor.fetchone()
        if item_avail:
            item_id = item_avail[0]
            cursor.execute(
                'UPDATE Items SET quantity = quantity + %s WHERE id = %d', (old_quantity, item_id)
            )
            cursor.execute(
                'UPDATE Items SET quantity = quantity - %s WHERE id = %d', (new_quantity, item_id)
            )
            mysql.connection.commit()
            msg = "Successfully item updated"
        else:
            msg = "Item selected is not available"
        # end if
        return cursor, mysql, msg
    
    @classmethod
    def delete_item_in_db(cls, cursor, mysql, data):
        itemname, quantity = data[0], data[1]
        store_add, store_city, store_state = data[2], data[3], data[4]

        # check if the input item is avaialble in db
        cursor.execute(
            'SELECT * FROM Items I, Stores S 
             WHERE I.location = %s AND I.itemname = %s AND I.quantity >= 0 
             AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s',
            (store_loc, itemname, state_add, state_city, state_state)
        )
        item_avail = cursor.fetchone()
        if item_avail:
            item_id = item_avail[0]
            cursor.execute(
                'UPDATE Items SET quantity = quantity + %s WHERE id = %d', (quantity, item_id)
            )
            mysql.connection.commit()
            msg = "Successfully item deleted"
        else:
            msg = "Item selected is not available"
        # end if
        return cursor, mysql, msg
    
    @classmethod
    def update_account_record(cls, cursor, mysql, data):
        pass

    
