# This script contains all methods that operates database

from macros import Macros
from utils import Utils

import os

class Database:

    @classmethod
    def create_account_table(cls, cursor, mysql):
        query = "CREATE DATABASE IF NOT EXISTS `grocerycart_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
        cursor.execute(query)
        query = "USE `grocerycart_db`;"
        cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) CHARSET=utf8;"
        cursor.execute(query)
        query = "INSERT INTO `accounts` (`username`, `password`, `email`) VALUES ('test_username', 'test_pw', 'test@test.com');"
        cursor.execute(query)
        mysql.connection.commit()
        return

    @classmethod
    def insert_account_record(cls, cursor, mysql, data):
        # query = "INSERT INTO `accounts` (`username`, `password`, `email`) VALUES ('test_username', 'test_pw', 'test@test.com');"
        # data: [hash_username, hash_password, email]
        if not os.path.exists(Macros.DB_FILE):
            cls.create_account_table(cursor, mysql)
        # end if
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

    
