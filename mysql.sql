-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: redkindle
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.12.04.1

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
-- Table structure for table `feeds`
--

DROP TABLE IF EXISTS `feeds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeds` (
  `f_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(80) DEFAULT NULL,
  `url` varchar(80) DEFAULT NULL,
  `isfulltext` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds`
--

LOCK TABLES `feeds` WRITE;
/*!40000 ALTER TABLE `feeds` DISABLE KEYS */;
INSERT INTO `feeds` VALUES (1,'aa','aaa',0),(2,'测试白啊','http://news.163.com/special/00011K6L/rss_newstop.xml',0),(3,'CNA','http://sports.163.com/special/00051K7F/rss_sportscba.xml',0),(4,'曹德吗','http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.fe',0);
/*!40000 ALTER TABLE `feeds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeds_user`
--

DROP TABLE IF EXISTS `feeds_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeds_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `k_id` int(10) unsigned DEFAULT NULL,
  `f_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds_user`
--

LOCK TABLES `feeds_user` WRITE;
/*!40000 ALTER TABLE `feeds_user` DISABLE KEYS */;
INSERT INTO `feeds_user` VALUES (5,1,1),(6,1,3),(7,1,2);
/*!40000 ALTER TABLE `feeds_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kinuser`
--

DROP TABLE IF EXISTS `kinuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kinuser` (
  `k_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `passwd` varchar(40) DEFAULT NULL,
  `kindle_email` varchar(40) DEFAULT NULL,
  `enable_send` tinyint(1) DEFAULT '0',
  `send_days` date DEFAULT NULL,
  `send_time` int(10) unsigned DEFAULT '0',
  `expires` date DEFAULT NULL,
  `timezone` int(11) DEFAULT '8',
  `keep_image` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`k_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kinuser`
--

LOCK TABLES `kinuser` WRITE;
/*!40000 ALTER TABLE `kinuser` DISABLE KEYS */;
INSERT INTO `kinuser` VALUES (1,'zzh','3fde6bb0541387e4ebdadf7c2ff31123','zzh123@126.com',0,NULL,11,NULL,-8,1);
/*!40000 ALTER TABLE `kinuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-16  5:18:26
