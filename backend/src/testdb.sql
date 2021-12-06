-- MySQL dump 10.13  Distrib 8.0.26, for macos11.3 (x86_64)
--
-- Host: localhost    Database: grocerycart_db
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Accounts`
--

DROP TABLE IF EXISTS `Accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Accounts`
--

LOCK TABLES `Accounts` WRITE;
/*!40000 ALTER TABLE `Accounts` DISABLE KEYS */;
INSERT INTO `Accounts` VALUES (1,'test_user','test_password','test@test.com'),(5,'f1e7c6edbfc5bfe10b38ada554c8fe25','aabe08dfc19121b315d1315a2f41d2ad','jxl115330@abc.com'),(13,'1024b4742936e6f8897fe577f948fb0b','7a6f5578ca92f74b7ad6aeefe6d46bfd','test@example.com');
/*!40000 ALTER TABLE `Accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Items`
--

DROP TABLE IF EXISTS `Items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store_id` int NOT NULL,
  `itemname` varchar(50) NOT NULL,
  `itemcode` varchar(20) NOT NULL,
  `price` float(8,3) NOT NULL,
  `expirydate` varchar(10) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemcode` (`itemcode`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `Stores` (`id`),
  CONSTRAINT `item_price_constraint` CHECK ((`price` >= 0.0)),
  CONSTRAINT `item_quantity_constraint` CHECK ((`quantity` >= 0.0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Items`
--

LOCK TABLES `Items` WRITE;
/*!40000 ALTER TABLE `Items` DISABLE KEYS */;
INSERT INTO `Items` VALUES (1,3,'apple','000000000001',0.800,'12012021',300),(2,3,'eggs brown medium grade a','000000000002',4.290,'12012021',200),(3,1,'fat free greek yogurt','000000000003',5.490,'11222021',200),(4,3,'broccoli florets','000000000004',2.590,'11222021',200),(5,4,'peanut butter crunchy','000000000005',4.100,'11222022',160),(6,4,'baby spinach salad','000000000006',2.290,'11222021',200),(7,1,'water spring','000000000007',0.890,'11192021',300),(8,2,'paper towels 6 pack','000000000008',6.490,'10102022',400),(9,5,'paper towels 6 pack','000000000009',6.490,'10102022',400),(10,6,'broccoli florets','000000000010',2.590,'11202021',200);
/*!40000 ALTER TABLE `Items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_date` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `items` varchar(20) NOT NULL,
  `order_type` varchar(20) NOT NULL,
  `price` float(8,3) NOT NULL,
  `address` varchar(50) DEFAULT NULL,
  `shipping_method` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Accounts` (`username`),
  CONSTRAINT `order_type_constraint` CHECK (((`order_type` = _utf8mb4'pickup') or (`order_type` = _utf8mb4'delivery'))),
  CONSTRAINT `price_constraint` CHECK ((`price` >= 0.0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Stores`
--

DROP TABLE IF EXISTS `Stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Stores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(100) NOT NULL,
  `loc_city` varchar(50) NOT NULL,
  `loc_state` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Stores`
--

LOCK TABLES `Stores` WRITE;
/*!40000 ALTER TABLE `Stores` DISABLE KEYS */;
INSERT INTO `Stores` VALUES (1,'3566 hardman road','dallas','TX'),(2,'1234 coit rd','richardson','TX'),(3,'6789 frankford rd','richardson','TX'),(4,'3456 w campbell rd','richardson','TX'),(5,'1339 edgewood avenue','addison','TX'),(6,'1629 Orchard Street','plano','TX');
/*!40000 ALTER TABLE `Stores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-06 10:25:42
