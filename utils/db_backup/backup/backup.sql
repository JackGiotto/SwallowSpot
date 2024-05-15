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
  `groupID` varchar(15) NOT NULL,
  PRIMARY KEY (`ID_telegram`),
  UNIQUE KEY `groupID` (`groupID`),
  KEY `fk_admin_user` (`ID_user`),
  CONSTRAINT `fk_admin_user` FOREIGN KEY (`ID_user`) REFERENCES `User` (`ID_user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES
('741878550',6,'1002134898283');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(1,'verde'),
(5,'viola');
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
) ENGINE=InnoDB AUTO_INCREMENT=262 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Criticalness`
--

LOCK TABLES `Criticalness` WRITE;
/*!40000 ALTER TABLE `Criticalness` DISABLE KEYS */;
INSERT INTO `Criticalness` VALUES
(214,1,1,1,51),
(215,1,2,1,51),
(216,1,3,1,51),
(217,2,1,1,51),
(218,2,2,1,51),
(219,2,3,1,51),
(220,3,1,1,51),
(221,3,2,1,51),
(222,3,3,1,51),
(223,4,1,1,51),
(224,4,2,1,51),
(225,4,3,1,51),
(226,5,1,1,51),
(227,5,2,1,51),
(228,5,3,1,51),
(229,6,1,2,51),
(230,6,2,1,51),
(231,6,3,1,51),
(232,7,1,2,51),
(233,7,2,1,51),
(234,7,3,1,51),
(235,8,1,2,51),
(236,8,2,1,51),
(237,8,3,1,51),
(238,1,1,1,52),
(239,1,2,1,52),
(240,1,3,1,52),
(241,2,1,1,52),
(242,2,2,1,52),
(243,2,3,1,52),
(244,3,1,2,52),
(245,3,2,2,52),
(246,3,3,1,52),
(247,4,1,1,52),
(248,4,2,1,52),
(249,4,3,1,52),
(250,5,1,1,52),
(251,5,2,1,52),
(252,5,3,1,52),
(253,6,1,2,52),
(254,6,2,1,52),
(255,6,3,1,52),
(256,7,1,1,52),
(257,7,2,1,52),
(258,7,3,1,52),
(259,8,1,1,52),
(260,8,2,1,52),
(261,8,3,1,52);
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
  `path` varchar(70) NOT NULL,
  PRIMARY KEY (`ID_report`),
  UNIQUE KEY `path` (`path`),
  UNIQUE KEY `starting_date` (`starting_date`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Report`
--

LOCK TABLES `Report` WRITE;
/*!40000 ALTER TABLE `Report` DISABLE KEYS */;
INSERT INTO `Report` VALUES
(51,'2024-01-07 14:00:00','2024-01-08 00:00:00','./static/bulletins/test.pdf'),
(52,'2024-02-09 14:00:00','2024-02-11 14:00:00','./static/bulletins/test2.pdf');
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
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Snow_criticalness`
--

LOCK TABLES `Snow_criticalness` WRITE;
/*!40000 ALTER TABLE `Snow_criticalness` DISABLE KEYS */;
INSERT INTO `Snow_criticalness` VALUES
(88,'2024-01-18 00:00:00',0,17,35),
(89,'2024-01-19 00:00:00',100,17,35),
(90,'2024-01-20 00:00:00',0,17,35),
(91,'2024-01-18 00:00:00',0,18,35),
(92,'2024-01-19 00:00:00',100,18,35),
(93,'2024-01-20 00:00:00',0,18,35),
(94,'2024-01-18 00:00:00',0,19,35),
(95,'2024-01-19 00:00:00',100,19,35),
(96,'2024-01-20 00:00:00',0,19,35),
(97,'2024-01-18 00:00:00',0,20,35),
(98,'2024-01-19 00:00:00',100,20,35),
(99,'2024-01-20 00:00:00',0,20,35),
(100,'2024-01-18 00:00:00',0,21,35),
(101,'2024-01-19 00:00:00',100,21,35),
(102,'2024-01-20 00:00:00',0,21,35);
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
(88,2,'0'),
(88,4,'0'),
(88,5,'0'),
(89,2,'5-10'),
(89,4,'10-15'),
(89,5,'10-15'),
(90,2,'0'),
(90,4,'0'),
(90,5,'0'),
(91,2,'0'),
(91,4,'0'),
(91,5,'0'),
(92,2,'5-10'),
(92,4,'10-15'),
(92,5,'10-15'),
(93,2,'0'),
(93,4,'0'),
(93,5,'0'),
(94,1,'0'),
(94,2,'0'),
(94,3,'0'),
(95,1,'2-10'),
(95,2,'5-10'),
(95,3,'10-15'),
(96,1,'0'),
(96,2,'0'),
(96,3,'0'),
(97,1,'0'),
(97,2,'0'),
(97,3,'0'),
(98,1,'2-10'),
(98,2,'5-15'),
(98,3,'10-20'),
(99,1,'0'),
(99,2,'0'),
(99,3,'0'),
(100,1,'0'),
(100,2,'0'),
(100,3,'0'),
(101,1,'2-10'),
(101,2,'5-15'),
(101,3,'10-20'),
(102,1,'0'),
(102,2,'0'),
(102,3,'0');
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
  `path` varchar(70) NOT NULL,
  PRIMARY KEY (`ID_snow_report`),
  UNIQUE KEY `path` (`path`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Snow_report`
--

LOCK TABLES `Snow_report` WRITE;
/*!40000 ALTER TABLE `Snow_report` DISABLE KEYS */;
INSERT INTO `Snow_report` VALUES
(35,'2024-01-18 00:00:00','./static/bulletins/test_snow.pdf');
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
(97,'Due Carrare',6),
(98,'Este',6),
(99,'Fontaniva',6),
(100,'Galliera Veneta',6),
(101,'Galzignano Terme',6),
(102,'Gazzo|',6),
(103,'Grantorto',6),
(104,'Granze',6),
(105,'Legnaro',6),
(106,'Limena',6),
(107,'Loreggia',6),
(108,'Lozzo Atestino',6),
(109,'Masera\' di Padova',6),
(110,'Masi',6),
(111,'Massanzago',7),
(112,'Megliadino San Vitale',6),
(113,'Merlara',6),
(114,'Mestrino',6),
(115,'Monselice',6),
(116,'Montagnana',6),
(117,'Montegrotto Terme',6),
(118,'Noventa Padovana',6),
(119,'Ospedaletto Euganeo',6),
(120,'Padova',6),
(121,'Pernumia',6),
(122,'Piacenza d\'Adige',6),
(123,'Piazzola sul Brenta',6),
(124,'Piombino Dese',7),
(125,'Piove di Sacco',6),
(126,'Polverara',6),
(127,'Ponso',6),
(128,'Ponte San Nicolo\'',6),
(129,'Pontelongo',6),
(130,'Pozzonovol',6),
(131,'Rovolon',6),
(132,'Rubano',6),
(133,'Saccolongo',6),
(134,'San Giorgio delle Pertiche',6),
(135,'San Giorgio in Bosco',6),
(136,'San Martino di Lupari',6),
(137,'San Pietro in Gu\'',6),
(138,'San Pietro Viminario',6),
(139,'Santa Giustina in Colle',6),
(140,'Sant\'Angelo di Piove di Sacco',6),
(141,'Sant\'Elena',6),
(142,'Sant\'Urbano',6),
(143,'Saonara',6),
(144,'Selvazzano Dentro',6),
(145,'Solesino',6),
(146,'Stanghella',6),
(147,'Teolo',6),
(148,'Terrassa Padovana',6),
(149,'Tombolo',6),
(150,'Torreglia',6),
(151,'Trebaseleghe',7),
(152,'Tribano',6),
(153,'Urbana',6),
(154,'Veggiano',6),
(155,'Vescovana',6),
(156,'Vighizzolo d\'Este',6),
(157,'Vigodarzere',6),
(158,'Vigonza',6),
(159,'Villa del Conte',6),
(160,'Villa Estense',6),
(161,'Villafranca Padovana',6),
(162,'Villanova di Camposampiero',7),
(163,'Vo\'',6),
(164,'Adria',5),
(165,'Ariano nel Polesine',5),
(166,'Arqua\' Polesine',5),
(167,'Badia Polesine',5),
(168,'Bagnolo di Po',5),
(169,'Bergantino',5),
(170,'Bosaro',5),
(171,'Calto',5),
(172,'Canaro',5),
(173,'Candal',5),
(174,'Castelguglielmo',5),
(175,'Castelmassa',5),
(176,'Castelnovo Bariano',5),
(177,'Ceneselli',5),
(178,'Ceregnano',5),
(179,'Corbola',5),
(180,'Costa di Rovigo',5),
(181,'Crespino',5),
(182,'Ficarolo',5),
(183,'Fiesso Umbertiano',5),
(184,'Frassinelle Polesine',5),
(185,'Fratta Polesine',5),
(186,'Gaiba',5),
(187,'Gavello',5),
(188,'Giacciano con Baruchella',5),
(189,'Guarda Veneta',5),
(190,'Lendinara',5),
(191,'Loreo',5),
(192,'Lusia',5),
(193,'Melara',5),
(194,'Occhiobello',5),
(195,'Papozze',5),
(196,'Pettorazza Grimani',5),
(197,'Pincara',5),
(198,'Polesella',5),
(199,'Pontecchio Polesine',5),
(200,'Porto Tolle',5),
(201,'Porto Viro',5),
(202,'Rosolina',5),
(203,'Rovigo',5),
(204,'Salara',5),
(205,'San Bellino',5),
(206,'San Martino di Venezze',5),
(207,'Stienta',5),
(208,'Taglio di Po',5),
(209,'Trecenta',5),
(210,'Villadose',5),
(211,'Villanova del Ghebbo',5),
(212,'Villanova Marchesana',5),
(213,'Villlamarzana',5),
(214,'Altivole',7),
(215,'Arcade',7),
(216,'Asolo',3),
(217,'Borso del Grappa',3),
(218,'Breda di Piave',7),
(219,'Caerano di San Marco',2),
(220,'Cappella Maggiore',2),
(221,'Carbonera',7),
(222,'Casale sul Sile',7),
(223,'Casier',7),
(224,'Castelcucco',3),
(225,'Castelfranco Veneto',6),
(226,'Castello di Godego',6),
(227,'Cavaso del Tomba',2),
(228,'Cessalto',8),
(229,'Chiarano',8),
(230,'Cimadolmo',7),
(231,'Cison di Valmarino',2),
(232,'Codogne\'',8),
(233,'Colle Umberto',2),
(234,'Conegliano',2),
(235,'Cordignano',2),
(236,'Cornuda',2),
(237,'Crocetta del Montello',2),
(238,'Farra di Soligo',2),
(239,'Follina',2),
(240,'Fontanelle',8),
(241,'Fonte',3),
(242,'Fregona',2),
(243,'Gaiarine',8),
(244,'Giavera del Montello',2),
(245,'Godega di Sant\'Urbano',8),
(246,'Gorgo al Monticano',8),
(247,'Istrana',7),
(248,'Loria',6),
(249,'Mansue\'',8),
(250,'Mareno di Piave',8),
(251,'Maser',2),
(252,'Maserada sul Piave',7),
(253,'Meduna di Livenza',8),
(254,'Miane',2),
(255,'Mogliano Veneto',7),
(256,'Monastier di Treviso',7),
(257,'Monfumo',3),
(258,'Montebelluna',2),
(259,'Morgano',7),
(260,'Moriago della Battaglia',2),
(261,'Motta di Livenza',8),
(262,'Nervesa della Battaglia',2),
(263,'Oderzo',8),
(264,'Ormelle',7),
(265,'Orsago',8),
(266,'Paese',7),
(267,'Pederobba',2),
(268,'Pieve del Grappa',3),
(269,'Pieve di Soligo',2),
(270,'Ponte di Piave',7),
(271,'Ponzano Veneto',7),
(272,'Portobuffole',8),
(273,'Possagno',2),
(274,'Povegliano',7),
(275,'Preganziol',7),
(276,'Quinto di Treviso',7),
(277,'Refrontolo',2),
(278,'Resana',6),
(279,'Revine Lago',2),
(280,'Riese Pio X',6),
(281,'Roncade',7),
(282,'Salgareda',7),
(283,'San Biagio di Callalta',7),
(284,'San Fior',2),
(285,'San Pietro di Feletto',2),
(286,'San Polo di Piave',7),
(287,'San Vendemiano',2),
(288,'San Zenone',3),
(289,'Santa Lucia di Piave',7),
(290,'Sarmede',2),
(291,'Segusino',2),
(292,'Sernaglia della Battaglia',2),
(293,'Silea',7),
(294,'Spresiano',7),
(295,'Susegana',2),
(296,'Tarzo',2),
(297,'Trevignano',7),
(298,'Treviso',7),
(299,'Valdobbiadene',2),
(300,'Vazzola',8),
(301,'Vedelago',7),
(302,'Vidor',2),
(303,'Villorba',7),
(304,'Vittorio Veneto',2),
(305,'Volpago del Montello',2),
(306,'Zenson di Piave',7),
(307,'Zero Branco',7),
(308,'Annone Veneto',8),
(309,'Campagna Lupia',7),
(310,'Campolongo Maggiore',6),
(311,'Camponogara',7),
(312,'Caorle',8),
(313,'Cavallino-Treporti',7),
(314,'Cavarzere',6),
(315,'Ceggia',8),
(316,'Chioggia',6),
(317,'Cinto Caomaggiore',8),
(318,'Cona',6),
(319,'Concordia Sagittaria',8),
(320,'Dolo',7),
(321,'Eraclea',7),
(322,'Fiesso d\'Artico',6),
(323,'Fossalta di Piave',7),
(324,'Fossalta di Portogruaro',8),
(325,'Fosso\'',6),
(326,'Gruaro',8),
(327,'Jesolo',7),
(328,'Marcon',7),
(329,'Martellago',7),
(330,'Meolo',7),
(331,'Mira',7),
(332,'Mirano',7),
(333,'Musile di Piave',7),
(334,'Noale',7),
(335,'Noventa di Piave',7),
(336,'Pianiga',7),
(337,'Portogruaro',8),
(338,'Pramaggiore',8),
(339,'Quarto d\'Altino',7),
(340,'Salzano',7),
(341,'San Dona\' di Piave',7),
(342,'San Michele al Tagliamento',8),
(343,'San Stino di Livenza',8),
(344,'Santa Maria di Sala',7),
(345,'Scorze\'',7),
(346,'Spinea',7),
(347,'Stra',6),
(348,'Teglio Veneto',8),
(349,'Torre di Mosto',8),
(350,'VENEZIA',7),
(351,'Vigonovo',6),
(352,'Agugliaro',6),
(353,'Albettone',6),
(354,'Alonte',6),
(355,'Altavilla Vicentina',3),
(356,'Altissimo',3),
(357,'Arcugnano',6),
(358,'Arsiero',3),
(359,'Arzignano',3),
(360,'Asiago',3),
(361,'Asigliano Veneto',6),
(362,'Barbarano Mossano',6),
(363,'Bassano del Grappa',3),
(364,'Bolzano Vicentino',3),
(365,'Breganze',3),
(366,'Brendola',6),
(367,'Bressanvido',3),
(368,'Brogliano',3),
(369,'Caldogno',3),
(370,'Caltrano',3),
(371,'Calvene',3),
(372,'Camisano Vicentino',6),
(373,'Campiglia dei Berici',6),
(374,'Carre\'',3),
(375,'Cartigliano',6),
(376,'Cassola',6),
(377,'Castegnero',6),
(378,'Castelgomberto',3),
(379,'Chiampo',3),
(380,'Chiuppano',3),
(381,'Cogollo del Cengio',3),
(382,'Colceresa',3),
(383,'Cornedo Vicentino',3),
(384,'Costabissara',3),
(385,'Creazzo',3),
(386,'Crespadoro',3),
(387,'Dueville',3),
(388,'Enego',3),
(389,'Fara Vicentino',3),
(390,'Foza',3),
(391,'Gallio',3),
(392,'Gambellara',3),
(393,'Gambugliano',3),
(394,'Grisignano di Zocco',6),
(395,'Grumolo delle Abbadesse',6),
(396,'Isola Vicentina',3),
(397,'Laghi',3),
(398,'Lastebasse',3),
(399,'Longare',3),
(400,'Lonigo',6),
(401,'Lugo di Vicenza',3),
(402,'Lusiana Conco',3),
(403,'Malo',3),
(404,'Marano Vicentino',3),
(405,'Marostica',3),
(406,'Monte di Malo',3),
(407,'Montebello Vicentino',3),
(408,'Montecchio Maggiore',3),
(409,'Montecchio Precalcino',3),
(410,'Montegalda',6),
(411,'Montegaldella',6),
(412,'Monteviale',3),
(413,'Monticello Conte Otto',3),
(414,'Montorso Vicentino',3),
(415,'Mussolente',3),
(416,'Nanto',6),
(417,'Nogarole Vicentino',3),
(418,'Nove',3),
(419,'Noventa Vicentina',6),
(420,'Orgiano',6),
(421,'Pedemonte',3),
(422,'Pianezze',3),
(423,'Piovene Rocchette',3),
(424,'Poiana Maggiore',6),
(425,'Posina',3),
(426,'Pove del Grappa',3),
(427,'Pozzoleone',6),
(428,'Quinto Vicentino',3),
(429,'Recoaro Terme',3),
(430,'Roana',3),
(431,'Romano d\'Ezzelino',3),
(432,'Rosa\'',6),
(433,'Rossano Veneto',6),
(434,'Rotzo',3),
(435,'Salcedo',3),
(436,'San Pietro Mussolino',3),
(437,'San Vito di Leguzzano',3),
(438,'Sandrigo',3),
(439,'Santorso',3),
(440,'Sarcedo',3),
(441,'Sarego',6),
(442,'Schiavon',3),
(443,'Schio',3),
(444,'Solagna',3),
(445,'Sossano',6),
(446,'Sovizzo',3),
(447,'Tezze sul Brenta',6),
(448,'Thiene',3),
(449,'Tonezza del Cimone',3),
(450,'Torrebelvicino',3),
(451,'Torri di Quartesolo',3),
(452,'Trissino',3),
(453,'Affi',4),
(454,'Albaredo d\'Adige',6),
(455,'Angiari',5),
(456,'Arcole',3),
(457,'Badia Calavena',4),
(458,'Bardolino',4),
(459,'Belfiore',4),
(460,'Bevilacqua',6),
(461,'Bonavigo',6),
(462,'Boschi Sant Anna',6),
(463,'Bosco Chiesanuova',4),
(464,'Bovolone',5),
(465,'Brentino Belluno',4),
(466,'Brenzone sul Garda',4),
(467,'Bussolengo',4),
(468,'Buttapietra',5),
(469,'Caldi ero',4),
(470,'Caprino Veronese',4),
(471,'Casaleone',5),
(472,'Castagnaro',5),
(473,'Castel d\'Azzano',5),
(474,'Castelnuovo del Garda',4),
(475,'Cavaion Veronese',4),
(476,'Cazzano di Tramigna',3),
(477,'Cerea',5),
(478,'Cerro Veronese',4),
(479,'Cologna Veneta',6),
(480,'Colognola ai Colli',4),
(481,'Concamarise',5),
(482,'Costermano sul Garda',4),
(483,'Dolce\'',4),
(484,'Erbe\'',5),
(485,'Erbezzo',4),
(486,'Ferrara di Monte Baldo',4),
(487,'Fumane',4),
(488,'Garda',4),
(489,'Gazzo Veronese',5),
(490,'Grezzana',4),
(491,'Illasi',4),
(492,'Isola della Scala',5),
(493,'Isola Rizza',5),
(494,'Lavagno',4),
(495,'Lazise',4),
(496,'Legnago',5),
(497,'Malcesine',4),
(498,'Marano di Valpolicella',4),
(499,'Mezzane di Sotto',4),
(500,'Minerbe',6),
(501,'Montecchia di Crosara',3),
(502,'Monteforte d\'Alpone',3),
(503,'Mozzecane',5),
(504,'Negrar',4),
(505,'Nogara',5),
(506,'Nogarole Rocca',5),
(507,'Oppeano',5),
(508,'Palu\'',5),
(509,'Pastrengo',4),
(510,'Pescantina',4),
(511,'Peschiera del Garda',4),
(512,'Povegliano Veronese',5),
(513,'Pressana',6),
(514,'Rivoli Veronese',4),
(515,'Ronca\'',3),
(516,'Ronco all\'Adige',4),
(517,'Roverchiara',5),
(518,'Rovere\' Veronese',4),
(519,'Roveredo di Gua\'',6),
(520,'Salizzole',5),
(521,'San Bonifacio',3),
(522,'San Giovanni Ilarione',3),
(523,'San Giovanni Lupatoto',5),
(524,'San Martino Buon Albergo',4),
(525,'San Mauro di Saline',4),
(526,'San Pietro di Morubio',5),
(527,'San Pietro in Cariano',4),
(528,'San Zeno di Montagna',4),
(529,'Sanguinetto',5),
(530,'Sant\'Ambrogio di Valpolicella',4),
(531,'Sant\'Anna d\'Alfaedo',4),
(532,'Selva di Progno',4),
(533,'Soave',3),
(534,'Sommacampagna',4),
(535,'Sona',4),
(536,'Sorga\'',5),
(537,'Terrazzo',6),
(538,'Torri del Benaco',4),
(539,'Tregnago',4),
(540,'Trevenzuolo',5),
(541,'Valeggio sul Mincio',4),
(542,'Velo Veronese',4),
(543,'Verona',4),
(544,'Veronella',6),
(545,'Vestenanova',3),
(546,'Vigasio',5),
(547,'Villa Bartolomea',5),
(548,'Villafranca di Verona',5),
(549,'Zevio',4),
(550,'Zimella',6);
/*!40000 ALTER TABLE `Topology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `ID_user` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(35) NOT NULL,
  `password` varchar(64) NOT NULL,
  `ID_area` int(11) NOT NULL,
  `ID_role` int(11) NOT NULL,
  PRIMARY KEY (`ID_user`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_user_area` (`ID_area`),
  KEY `fk_user_role` (`ID_role`),
  CONSTRAINT `fk_user_area` FOREIGN KEY (`ID_area`) REFERENCES `Area` (`ID_area`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_role` FOREIGN KEY (`ID_role`) REFERENCES `Role` (`ID_role`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES
(5,'giacomo','bedd18fc5eb32c050cd3a9ce7b27892a661760e4bf3ba8f38dd4f6858f3951ee',6,3),
(6,'leo','a598174a3d25e5f4a1c9aa5e6634127c4b9b698b6ec94c5998fa6514d2ea9726',7,3),
(7,'davide','7483119d8b8d25d8ce6d8e5812c67abd860ff89f922feacd762ec4cd130feb16',3,3),
(9,'stefani','68c232adb20e0e658edaa0499e6011ca0c061b4358a89fad6b9a046748789efd',7,3),
(13,'tommaso','8ffbeac20731de54ac2d7d4c3d811c7c900b279f9b917a6ccd3df29b2820cb63',6,3),
(29,'marco','7cf4537051f00c77eb33543a62239c7a873f54715bc3c399a3011d01c74d09a9',3,1),
(35,'testingaccount','086f9ac66be6c6c8d495e440ea11d86d566bf77beda966491577425a293f930e',3,2);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-14 22:16:07
