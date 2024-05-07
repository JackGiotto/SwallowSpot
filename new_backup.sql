-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Swallow Spot
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Admin` (
  `ID_telegram` varchar(15) NOT NULL,
  `ID_user` int(11) NOT NULL,
  PRIMARY KEY (`ID_telegram`),
  KEY `fk_admin_user` (`ID_user`),
  CONSTRAINT `fk_admin_user` FOREIGN KEY (`ID_user`) REFERENCES `User` (`ID_user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Altitude`
--

DROP TABLE IF EXISTS `Altitude`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Altitude` (
  `ID_altitude` int(11) NOT NULL AUTO_INCREMENT,
  `height` varchar(10) NOT NULL,
  PRIMARY KEY (`ID_altitude`),
  UNIQUE KEY `height` (`height`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Altitude`
--

LOCK TABLES `Altitude` WRITE;
/*!40000 ALTER TABLE `Altitude` DISABLE KEYS */;
INSERT INTO `Altitude` VALUES
(1,'1000 m'),
(2,'1500 m'),
(4,'2000 m'),
(3,'>1500 m'),
(5,'>2000 m');
/*!40000 ALTER TABLE `Altitude` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Area`
--

DROP TABLE IF EXISTS `Area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Area` (
  `ID_area` int(11) NOT NULL AUTO_INCREMENT,
  `area_name` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_area`),
  UNIQUE KEY `area_name` (`area_name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Area`
--

LOCK TABLES `Area` WRITE;
/*!40000 ALTER TABLE `Area` DISABLE KEYS */;
INSERT INTO `Area` VALUES
(17,'Alto Agordino'),
(21,'Altopiano dei sette comuni'),
(19,'Cadore'),
(20,'Feltrino-Val Belluna'),
(18,'Medio-Basso Agordino'),
(9,'Mont-1A'),
(10,'Mont-1B'),
(11,'Mont-1C'),
(12,'Mont-1D'),
(13,'Mont-2A'),
(14,'Mont-2B'),
(15,'Mont-2C'),
(16,'Mont-2D'),
(1,'Vene-A'),
(3,'Vene-B'),
(4,'Vene-C'),
(5,'Vene-D'),
(6,'Vene-E'),
(7,'Vene-F'),
(8,'Vene-G'),
(2,'Vene-H');
/*!40000 ALTER TABLE `Area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Color`
--

DROP TABLE IF EXISTS `Color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Color` (
  `ID_color` int(11) NOT NULL AUTO_INCREMENT,
  `color_name` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_color`),
  UNIQUE KEY `color_name` (`color_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Color`
--

LOCK TABLES `Color` WRITE;
/*!40000 ALTER TABLE `Color` DISABLE KEYS */;
INSERT INTO `Color` VALUES
(3,'arancio'),
(2,'gialla'),
(4,'rossa'),
(1,'verde');
/*!40000 ALTER TABLE `Color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Criticalness`
--

DROP TABLE IF EXISTS `Criticalness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Criticalness` (
  `ID_issue` int(11) NOT NULL AUTO_INCREMENT,
  `ID_area` int(11) NOT NULL,
  `ID_risk` int(11) NOT NULL,
  `ID_color` int(11) NOT NULL,
  `ID_report` int(11) NOT NULL,
  PRIMARY KEY (`ID_issue`),
  KEY `fk_criticalness_area` (`ID_area`),
  KEY `fk_criticalness_risk` (`ID_risk`),
  KEY `fk_criticalness_color` (`ID_color`),
  KEY `fk_criticalness_report` (`ID_report`),
  CONSTRAINT `fk_criticalness_area` FOREIGN KEY (`ID_area`) REFERENCES `Area` (`ID_area`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_criticalness_color` FOREIGN KEY (`ID_color`) REFERENCES `Color` (`ID_color`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_criticalness_report` FOREIGN KEY (`ID_report`) REFERENCES `Report` (`ID_report`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_criticalness_risk` FOREIGN KEY (`ID_risk`) REFERENCES `Risk` (`ID_risk`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Criticalness`
--

LOCK TABLES `Criticalness` WRITE;
/*!40000 ALTER TABLE `Criticalness` DISABLE KEYS */;
INSERT INTO `Criticalness` VALUES
(118,1,1,1,47),
(119,1,2,1,47),
(120,1,3,1,47),
(121,2,1,1,47),
(122,2,2,1,47),
(123,2,3,1,47),
(124,3,1,1,47),
(125,3,2,1,47),
(126,3,3,1,47),
(127,4,1,1,47),
(128,4,2,1,47),
(129,4,3,1,47),
(130,5,1,1,47),
(131,5,2,1,47),
(132,5,3,1,47),
(133,6,1,2,47),
(134,6,2,1,47),
(135,6,3,1,47),
(136,7,1,2,47),
(137,7,2,1,47),
(138,7,3,1,47),
(139,8,1,2,47),
(140,8,2,1,47),
(141,8,3,1,47),
(142,1,1,1,48),
(143,1,2,1,48),
(144,1,3,1,48),
(145,2,1,1,48),
(146,2,2,1,48),
(147,2,3,1,48),
(148,3,1,2,48),
(149,3,2,2,48),
(150,3,3,1,48),
(151,4,1,1,48),
(152,4,2,1,48),
(153,4,3,1,48),
(154,5,1,1,48),
(155,5,2,1,48),
(156,5,3,1,48),
(157,6,1,2,48),
(158,6,2,1,48),
(159,6,3,1,48),
(160,7,1,1,48),
(161,7,2,1,48),
(162,7,3,1,48),
(163,8,1,1,48),
(164,8,2,1,48),
(165,8,3,1,48);
/*!40000 ALTER TABLE `Criticalness` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Report`
--

DROP TABLE IF EXISTS `Report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Report` (
  `ID_report` int(11) NOT NULL AUTO_INCREMENT,
  `starting_date` datetime NOT NULL,
  `ending_date` datetime NOT NULL,
  `path` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_report`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Report`
--

LOCK TABLES `Report` WRITE;
/*!40000 ALTER TABLE `Report` DISABLE KEYS */;
INSERT INTO `Report` VALUES
(47,'2024-01-07 14:00:00','2024-01-08 00:00:00','./bulletins/test.pdf'),
(48,'2024-02-09 14:00:00','2024-02-11 14:00:00','./bulletins/test2.pdf');
/*!40000 ALTER TABLE `Report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Risk`
--

DROP TABLE IF EXISTS `Risk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Risk` (
  `ID_risk` int(11) NOT NULL AUTO_INCREMENT,
  `risk_name` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_risk`),
  UNIQUE KEY `risk_name` (`risk_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Risk`
--

LOCK TABLES `Risk` WRITE;
/*!40000 ALTER TABLE `Risk` DISABLE KEYS */;
INSERT INTO `Risk` VALUES
(1,'idraulico'),
(2,'idrogeologico'),
(3,'idrogeologico con temporali');
/*!40000 ALTER TABLE `Risk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Role`
--

DROP TABLE IF EXISTS `Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Role` (
  `ID_role` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_role`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Role`
--

LOCK TABLES `Role` WRITE;
/*!40000 ALTER TABLE `Role` DISABLE KEYS */;
INSERT INTO `Role` VALUES
(2,'admin'),
(1,'normal'),
(3,'super-admin');
/*!40000 ALTER TABLE `Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Snow_criticalness`
--

DROP TABLE IF EXISTS `Snow_criticalness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Snow_criticalness` (
  `ID_snow_issue` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `percentage` int(11) NOT NULL,
  `ID_area` int(11) NOT NULL,
  `ID_snow_report` int(11) NOT NULL,
  PRIMARY KEY (`ID_snow_issue`),
  KEY `fk_snow_criticalness_report` (`ID_snow_report`),
  KEY `fk_snow_criticalness_area` (`ID_area`),
  CONSTRAINT `fk_snow_criticalness_area` FOREIGN KEY (`ID_area`) REFERENCES `Area` (`ID_area`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_snow_criticalness_report` FOREIGN KEY (`ID_snow_report`) REFERENCES `Snow_report` (`ID_snow_report`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Snow_criticalness`
--

LOCK TABLES `Snow_criticalness` WRITE;
/*!40000 ALTER TABLE `Snow_criticalness` DISABLE KEYS */;
INSERT INTO `Snow_criticalness` VALUES
(58,'2024-01-18 00:00:00',0,17,33),
(59,'2024-01-19 00:00:00',100,17,33),
(60,'2024-01-20 00:00:00',0,17,33),
(61,'2024-01-18 00:00:00',0,18,33),
(62,'2024-01-19 00:00:00',100,18,33),
(63,'2024-01-20 00:00:00',0,18,33),
(64,'2024-01-18 00:00:00',0,19,33),
(65,'2024-01-19 00:00:00',100,19,33),
(66,'2024-01-20 00:00:00',0,19,33),
(67,'2024-01-18 00:00:00',0,20,33),
(68,'2024-01-19 00:00:00',100,20,33),
(69,'2024-01-20 00:00:00',0,20,33),
(70,'2024-01-18 00:00:00',0,21,33),
(71,'2024-01-19 00:00:00',100,21,33),
(72,'2024-01-20 00:00:00',0,21,33);
/*!40000 ALTER TABLE `Snow_criticalness` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Snow_criticalness_altitude`
--

DROP TABLE IF EXISTS `Snow_criticalness_altitude`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Snow_criticalness_altitude` (
  `ID_snow_issue` int(11) NOT NULL,
  `ID_altitude` int(11) NOT NULL,
  `value` varchar(15) NOT NULL,
  PRIMARY KEY (`ID_snow_issue`,`ID_altitude`),
  KEY `fk_altitude` (`ID_altitude`),
  CONSTRAINT `fk_altitude` FOREIGN KEY (`ID_altitude`) REFERENCES `Altitude` (`ID_altitude`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_snow_issue` FOREIGN KEY (`ID_snow_issue`) REFERENCES `Snow_criticalness` (`ID_snow_issue`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Snow_criticalness_altitude`
--

LOCK TABLES `Snow_criticalness_altitude` WRITE;
/*!40000 ALTER TABLE `Snow_criticalness_altitude` DISABLE KEYS */;
INSERT INTO `Snow_criticalness_altitude` VALUES
(58,2,'0'),
(58,4,'0'),
(58,5,'0'),
(59,2,'5-10'),
(59,4,'10-15'),
(59,5,'10-15'),
(60,2,'0'),
(60,4,'0'),
(60,5,'0'),
(61,2,'0'),
(61,4,'0'),
(61,5,'0'),
(62,2,'5-10'),
(62,4,'10-15'),
(62,5,'10-15'),
(63,2,'0'),
(63,4,'0'),
(63,5,'0'),
(64,1,'0'),
(64,2,'0'),
(64,3,'0'),
(65,1,'2-10'),
(65,2,'5-10'),
(65,3,'10-15'),
(66,1,'0'),
(66,2,'0'),
(66,3,'0'),
(67,1,'0'),
(67,2,'0'),
(67,3,'0'),
(68,1,'2-10'),
(68,2,'5-15'),
(68,3,'10-20'),
(69,1,'0'),
(69,2,'0'),
(69,3,'0'),
(70,1,'0'),
(70,2,'0'),
(70,3,'0'),
(71,1,'2-10'),
(71,2,'5-15'),
(71,3,'10-20'),
(72,1,'0'),
(72,2,'0'),
(72,3,'0');
/*!40000 ALTER TABLE `Snow_criticalness_altitude` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Snow_report`
--

DROP TABLE IF EXISTS `Snow_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Snow_report` (
  `ID_snow_report` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `path` varchar(35) NOT NULL,
  PRIMARY KEY (`ID_snow_report`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Snow_report`
--

LOCK TABLES `Snow_report` WRITE;
/*!40000 ALTER TABLE `Snow_report` DISABLE KEYS */;
INSERT INTO `Snow_report` VALUES
(33,'2024-01-18 00:00:00','./bulletins/test_snow.pdf');
/*!40000 ALTER TABLE `Snow_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Topology`
--

DROP TABLE IF EXISTS `Topology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Topology` (
  `ID_city` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(35) NOT NULL,
  `ID_area` int(11) NOT NULL,
  PRIMARY KEY (`ID_city`),
  UNIQUE KEY `city_name` (`city_name`),
  KEY `fk_topology_area` (`ID_area`),
  CONSTRAINT `fk_topology_area` FOREIGN KEY (`ID_area`) REFERENCES `Area` (`ID_area`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=551 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Topology`
--

LOCK TABLES `Topology` WRITE;
/*!40000 ALTER TABLE `Topology` DISABLE KEYS */;
INSERT INTO `Topology` VALUES
(1,'Agorca',1),
(2,'Alano di Piave',2),
(3,'Alleghe',1),
(4,'Alpago',2),
(5,'Arsie',3),
(6,'Auronzo di Cadore',1),
(7,'Belluno',2),
(8,'Borca di Cadore',1),
(9,'Borgo Valbelluna',2),
(10,'Calalzo di Cadore',1),
(11,'Canale d Agordo',1),
(12,'Cencenighe Agordino',1),
(13,'Cesiomaggiore',2),
(14,'Chies d\'Alpago',2),
(15,'Cibiana di Cadore',1),
(16,'Colle Santa Lucia',1),
(17,'Comelico Superiore',1),
(18,'Cortina d\'Ampezzo',1),
(19,'Danta di Cadore',1),
(20,'Domegge di Cadore',1),
(21,'Falcade',1),
(22,'Feltre',2),
(23,'Fonzaso',3),
(24,'Cosaldo',1),
(25,'La Valle Agordina',1),
(26,'Lamon',3),
(27,'Limana',2),
(28,'Livinallongo del Col di Lana',1),
(29,'Longarone',1),
(30,'Lorenzago di Cadore',1),
(31,'Lozzo di Cadore',1),
(32,'Ospitale di Cadore',1),
(33,'Pedavena',2),
(34,'Perarolo di Cadore',1),
(35,'Pieve di Cadore',1),
(36,'Ponte nelle Alpi',2),
(37,'Quero Vas',2),
(38,'Rivamonte Agordino',1),
(39,'Rocca Pietore',1),
(40,'San Gregorio nelle Alpi',2),
(41,'San Nicolo\' di Comelico',1),
(42,'San Pietro di Cadore',1),
(43,'San Tomaso Agordino',1),
(44,'San Vito di Cadore',1),
(45,'Santa Giustina',2),
(46,'Santo Stefano di Cadore',1),
(47,'Sedico',2),
(48,'Selva di Cadore',1),
(49,'Seren del Grappa',2),
(50,'Sospirolo',2),
(51,'Soverzene',2),
(52,'Sovramonte',3),
(53,'Taibon Agordino',1),
(54,'Tambre',2),
(55,'Val di Zoldo',1),
(56,'Vallada Agordina',1),
(57,'Valle di Cadore',1),
(58,'Vigo di Cadore',1),
(59,'Vodo Cadore',1),
(60,'Voltago Agordino',1),
(61,'Zoppe\' di Cadore',1),
(62,'Abano Terme',6),
(63,'Agna',6),
(64,'Albignasego',6),
(65,'Anguillara Veneta',6),
(66,'Arqua\' Petrarca',6),
(67,'Arre',6),
(68,'Arzergrande',6),
(69,'Bagnoli di Sopra',6),
(70,'Baone',6),
(71,'Barbona',6),
(72,'Battaglia Terme',6),
(73,'Boara Pisani',6),
(74,'Borgo Veneto',6),
(75,'Borgoricco',6),
(76,'Bovolenta',6),
(77,'Brugine',6),
(78,'Cadoneghe',6),
(79,'Campo San Martino',6),
(80,'Campodarsego',6),
(81,'Campodoro',6),
(82,'Camposampiero',6),
(83,'Candiana',6),
(84,'Carceri',6),
(85,'Carmignano di Brenta',6),
(86,'Cartura',6),
(87,'Casale di Scodosia',6),
(88,'Casalserugo',6),
(89,'Castelbaldo',6),
(90,'Cervarese Santa Croce',6),
(91,'Cinto Euganeo',6),
(92,'Cittadella',6),
(93,'Codevigo',6),
(94,'Conselve',6),
(95,'Correzzola',6),
(96,'Curtarolo',6),
(97,'