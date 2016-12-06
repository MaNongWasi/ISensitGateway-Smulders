-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: isensit_gw
-- ------------------------------------------------------
-- Server version	5.5.44-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acc_beacons`
--

DROP TABLE IF EXISTS `acc_beacons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acc_beacons` (
  `row_count` int(30) NOT NULL AUTO_INCREMENT,
  `beacon_id` int(11) NOT NULL,
  `beacon_accx` float NOT NULL,
  `beacon_accy` float NOT NULL,
  `beacon_accz` float NOT NULL,
  `beacon_rssi` int(11) NOT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  `beacon_accsum` float NOT NULL,
  `pitch` float NOT NULL,
  `roll` float NOT NULL,
  `levelPitch` int(2) NOT NULL,
  `levelRoll` int(2) NOT NULL,
  `levelPitch1` int(11) DEFAULT NULL,
  `levelPitch2` int(11) DEFAULT NULL,
  `levelPitch3` int(11) DEFAULT NULL,
  `levelPitch4` int(11) DEFAULT NULL,
  `levelRoll1` int(11) DEFAULT NULL,
  `levelRoll2` int(11) DEFAULT NULL,
  `levelRoll3` int(11) DEFAULT NULL,
  `levelRoll4` int(11) DEFAULT NULL,
  `levelRoll5` int(11) DEFAULT NULL,
  `teller` int(11) DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=1521762 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `fd_sensors`
--

DROP TABLE IF EXISTS `fd_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fd_sensors` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT, 
  `fd_id` varchar(11) NOT NULL,
  `pm` float DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `hum` float DEFAULT NULL,
  `pm_hour` float DEFAULT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `noise_sensors`
--

DROP TABLE IF EXISTS `noise_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `noise_sensors` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT,
  `noise_id` varchar(11) NOT NULL,
  `sensor_db` float(10,1) DEFAULT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=267 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT,
  `beacon_id` int(11) DEFAULT NULL,
  `cal_val` float(10,2) NOT NULL,
  `pitch_cal` float NOT NULL,
  `roll_cal` float NOT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
-- Dump completed on 2016-09-09 12:51:01


--
-- Table structure for table `rssi`
--

DROP TABLE IF EXISTS `rssi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rssi` (
  `row_count` int(11) NOT NULL AUTO_INCREMENT,
  `beacon_id` int(11) DEFAULT NULL,
  `rssi` int(5) DEFAULT NULL,
  `created_at` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`row_count`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rssi`

