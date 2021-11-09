# This script contains all methods that operates database

from macros import Macros
from utils import Utils

import os

class Database:

    def create_account_table(cursor):
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;"
        cursor.execute(query)
        return

    def insert_account_record(cursor, mysql, data):
        # query = "INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test_username', 'test_pw', 'test@test.com');"
        # data: [hash_username, hash_password, email]
        if not os.path.exists(Macros.DB_FILE):
            cls.create_account_table(cursor)
        # end if
        query = cursor.execute(
            'INSERT INTO accounts VALUES (NULL, %s, %s, %s)',
            (data[0], data[1], data[2],)
        )
        mysql.connection.commit()
        return cursor, mysql

    def delete_account_record(cursor, mysql, data):
        pass

    def update_account_record(cursor, mysql, data):
        pass

    
