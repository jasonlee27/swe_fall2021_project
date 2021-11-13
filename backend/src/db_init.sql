CREATE DATABASE IF NOT EXISTS `grocerycart_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `grocerycart_db`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');

CREATE TABLE IF NOT EXISTS `items` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`itemname` varchar(50) NOT NULL,
  	`itemcode` varchar(255) NOT NULL,
  	`price` varchar(100) NOT NULL,
        `expirydate` varchar(100) NOT NULL,
        `quantity` varchar(100) NOT NULL,
        `location` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (1, 'apple', '000000000001', '0.8', '12012021', '300', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (2, 'eggs brown medium grade a', '000000000002', '4.29', '12012021', '200', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (3, 'fat free greek yogurt', '000000000003', '5.49', '11222021', '200', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (4, 'broccoli florets', '000000000004', '2.59', '11222021', '200', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (5, 'peanut butter crunchy', '000000000005', '4.19', '11222022', '160', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (6, 'baby spinach salad', '000000000006', '2.29', '11222021', '200', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (7, 'water spring', '000000000007', '0.89', '11192021', '300', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (8, 'paper towels 6 pack', '000000000008', '6.49', '10102022', '400', 'richardson');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (9, 'paper towels 6 pack', '000000000008', '6.49', '10102022', '400', 'dallas');
INSERT INTO `items` (`id`, `itemname`, `itemcode`, `price`, `expirydate`, `quantity`, `location`) VALUES (10, 'broccoli florets', '000000000004', '2.59', '11202021', '200', 'dallas');
