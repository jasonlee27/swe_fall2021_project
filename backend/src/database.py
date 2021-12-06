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
            'INSERT IGNORE INTO Accounts (username, password, email) VALUES (%s, %s, %s)',
            (data[0], data[1], data[2])
        )
        mysql.connection.commit()
        return cursor, mysql

    @classmethod
    def insert_account_record(cls, cursor, mysql, data):
        # query = "INSERT INTO `accounts` (`username`, `password`, `email`) VALUES ('test_username', 'test_pw', 'test@test.com');"
        # data: [hash_username, hash_password, email]
        cursor.execute(
            'INSERT IGNORE INTO Accounts (username, password, email) VALUES (%s, %s, %s)',
            (data[0], data[1], data[2])
        )
        mysql.connection.commit()
        return cursor, mysql

    @classmethod
    def get_user_info(cls, cursor, mysql, data):
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
    def get_all_stores_in_db(cls, cursor, mysql):
        cursor.execute('SELECT * FROM Stores')
        stores = cursor.fetchall()
        if stores:
            return stores
        # end if
        return
    
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
    def add_item_order(cls, cursor, mysql, data):
        itemcode, quantity = data[0], data[1]
        store_address, store_city, store_state = data[2], data[3], data[4]
        item_price = 0.
        item_name = ''
        # check if the input item is avaialble in db
        cursor.execute(
            """SELECT I.id, I.price, I.itemname FROM Items I, Stores S 
             WHERE I.itemcode = %s AND I.quantity >= %s 
             AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s""",
            (store_loc, itemcode, quantity, store_address, store_city, store_state)
        )
        item_avail = cursor.fetchone()
        if item_avail:
            item_id = item_avail[0]
            item_price = item_avail[1]
            item_name = item_avail[2]
            cursor.execute(
                'UPDATE Items SET quantity = quantity - %s WHERE id = %d', (quantity, item_id)
            )
            mysql.connection.commit()
            msg = "Successfully item added"
        else:
            msg = "Item selected is not available"
        # end if
        return cursor, mysql, msg, item_name, item_price

    @classmethod
    def update_item_order(cls, cursor, mysql, data):
        itemcode, old_quantity, new_quantity, old_total_price = data[0], data[1], data[2], data[3]
        store_address, store_city, store_state = data[4], data[5], data[6]
        item_price, new_total_price = 0., 0.
        item_name = ''
        # check if the input item is avaialble in db
        if old_quantity>new_quantity: # deletion
            cursor.execute(
                """SELECT I.id, I.price, I.itemname FROM Items I, Stores S 
                WHERE I.itemcode = %s AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s""",
                (itemcode, state_add, state_city, state_state)
            )
            item_avail = cursor.fetchone()
            if item_avail:
                item_id = item_avail[0]
                item_price = item_avail[1]
                item_name = item_avail[2]
                cursor.execute(
                    'UPDATE Items SET quantity = quantity + %s WHERE id = %d', (old_quantity-new_quantity, item_id)
                )
                mysql.connection.commit()
                new_total_price =  old_total_price - item_price*(old_quantity-new_quantity)
                msg = "Successfully item updated"
            else:
                msg = "Item selected is not available"
            # end if
        elif old_quantity<new_quantity: # addition
            cursor.execute(
                """SELECT I.id, I.price, I.itemname FROM Items I, Stores S 
                WHERE I.itemcode = %s AND I.quantity >= %s 
                AND S.id=I.store_id AND S.address = %s AND S.loc_city = %s AND S.loc_state = %s""",
                (itemcode, new_quantity-old_quantity, store_address, store_city, store_state)
            )
            item_avail = cursor.fetchone()
            if item_avail:
                item_id = item_avail[0]
                item_price = item_avail[1]
                item_name = item_avail[2]
                cursor.execute(
                    'UPDATE Items SET quantity = quantity - %s WHERE id = %d', (new_quantity-old_quantity, item_id)
                )
                mysql.connection.commit()
                new_total_price =  old_total_price + item_price*(new_quantity-old_quantity)
                msg = "Successfully item updated"
            else:
                msg = "Item selected is not available"
            # end if
        # end if
        return cursor, mysql, msg, item_name, item_price, new_total_price
    
    @classmethod
    def insert_order_record(cls, cursor, mysql, data):
        username, item_list, order_type, price = data[0], data[1], data[2], data[3]
        shipping_address, shipping_method = None, None
        item_str = "|".join([f"{item[0]}::{item[1]}" for item in item_list])
        if order_type == "delivery":
            shipping_address, shipping_method = data[4], data[5]
        # end if
        order_time = Utils.get_cur_time()
        cursor.execute(
            """INSERT INTO Orders (order_date, username, items, order_type, price, address, shipping_method) VALUES (%s, %s, %s)""",
            (order_time, username, item_str, order_type, str(price), shipping_address, shipping_method)
        )
        mysql.connection.commit()
        msg = "Order confirmed"
        return cursor, mysql, msg
