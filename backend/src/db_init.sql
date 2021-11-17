CREATE DATABASE IF NOT EXISTS `grocerycart_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `grocerycart_db`;


-- Account Table
CREATE TABLE IF NOT EXISTS Accounts (
       id int(11) NOT NULL AUTO_INCREMENT,
       username varchar(50) NOT NULL,
       password varchar(50) NOT NULL,
       email varchar(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(username)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO Accounts (id, username, password, email) VALUES (1, 'test', 'test@test.com');


-- Store Table
CREATE TABLE IF NOT EXISTS Stores (
	id int(11) NOT NULL AUTO_INCREMENT,
        address varchar(100) NOT NULL,
  	loc_city varchar(50) NOT NULL,
  	loc_state varchar(2) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO Stores (id, loc_city, loc_state) VALUES (1, '3566 hardman road', 'dallas', 'TX');
INSERT INTO Stores (id, loc_city, loc_state) VALUES (2, '1234 coit rd', 'richardson', 'TX');
INSERT INTO Stores (id, loc_city, loc_state) VALUES (3, '6789 frankford rd', 'richardson', 'TX');
INSERT INTO Stores (id, loc_city, loc_state) VALUES (4, '3456 w campbell rd', 'richardson', 'TX');
INSERT INTO Stores (id, loc_city, loc_state) VALUES (5, '1339 edgewood avenue', 'addison', 'TX');
INSERT INTO Stores (id, loc_city, loc_state) VALUES (6, '1629 Orchard Street', 'plano', 'TX');


-- Item Table
CREATE TABLE IF NOT EXISTS Items (
	id int(11) NOT NULL AUTO_INCREMENT,
        store_id int(11) NOT NULL,
  	itemname varchar(50) NOT NULL,
  	itemcode varchar(20) NOT NULL,
  	price float(8,3) NOT NULL,
        expirydate varchar(10) NOT NULL,
        quantity int(10) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (itemcode),
    FOREIGN KEY (store_id) REFERENCES Stores(id),
    CONSTRAINT item_quantity_constraint CHECK (quantity>=0.0)
    CONSTRAINT item_price_constraint CHECK (price>=0.0)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (1, 3, 'apple', '000000000001', 0.8, '12012021', 300);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (2, 3, 'eggs brown medium grade a', '000000000002', 4.29, '12012021', 200);
INSERT INTO Items (id, itemname, itemcode, price, expirydate, quantity) VALUES (3, 'fat free greek yogurt', '000000000003', 5.49, '11222021', 200);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (4, 3, 'broccoli florets', '000000000004', 2.59, '11222021', 200);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (5, 4, 'peanut butter crunchy', '000000000005', 4.1, '11222022', 160);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (6, 4, 'baby spinach salad', '000000000006', 2.29, '11222021', 200);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (7, 1, 'water spring', '000000000007', 0.89, '11192021', 300);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (8, 2, 'paper towels 6 pack', '000000000008', 6.49, '10102022', 400);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (9, 5, 'paper towels 6 pack', '000000000008', 6.49, '10102022', 400);
INSERT INTO Items (id, store_id, itemname, itemcode, price, expirydate, quantity) VALUES (10, 6, 'broccoli florets', '000000000004', 2.59, '11202021', 200);


-- Order Table
CREATE TABLE IF NOT EXISTS Orders (
	id int(11) NOT NULL AUTO_INCREMENT,
  	order_date varchar(50) NOT NULL,
        username  varchar(20) NOT NULL,
  	items varchar(20) NOT NULL,
        order_type varchar(20) NOT NULL,
        price float(8,3) NOT NULL,
        address varchar(50)
        shipping_method varchar(20),
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES Accounts(username),
    CONSTRAINT order_type_constraint CHECK (order_type = 'pickup' OR order_type = 'delivery'),
    CONSTRAINT price_constraint CHECK (price>=0.0),
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
