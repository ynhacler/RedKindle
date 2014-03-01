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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `c_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `category_name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'资讯'),(2,'博客'),(3,'学习'),(4,'娱乐'),(5,'杂志'),(6,'文化'),(7,'科技'),(8,'财经'),(9,'生活'),(10,'文化');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeds`
--

DROP TABLE IF EXISTS `feeds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeds` (
  `f_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(80) DEFAULT NULL,
  `url` varchar(150) DEFAULT NULL,
  `isfulltext` tinyint(1) DEFAULT '0',
  `c_id` int(10) unsigned DEFAULT NULL,
  `descrip` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds`
--

LOCK TABLES `feeds` WRITE;
/*!40000 ALTER TABLE `feeds` DISABLE KEYS */;
INSERT INTO `feeds` VALUES (1,'aa','aaa',0,NULL,NULL),(2,'测试白啊','http://news.163.com/special/00011K6L/rss_newstop.xml',0,NULL,NULL),(3,'CNA','http://sports.163.com/special/00051K7F/rss_sportscba.xml',0,NULL,NULL),(5,'qwq','qqqq',0,NULL,NULL),(6,'sdafa','asdfsafasf',1,NULL,NULL),(7,'豆瓣','DoubanBook',0,NULL,NULL),(8,'知乎日报','ZhihuDaily',0,NULL,NULL),(9,'wwwwwwww','ewwwwww',1,6,'nishi谁奥斯卡大家\r\n	    ');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds_user`
--

LOCK TABLES `feeds_user` WRITE;
/*!40000 ALTER TABLE `feeds_user` DISABLE KEYS */;
INSERT INTO `feeds_user` VALUES (8,1,3),(9,1,8),(10,1,1);
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
  `name` varchar(50) DEFAULT NULL,
  `passwd` varchar(40) DEFAULT NULL,
  `kindle_email` varchar(50) DEFAULT NULL,
  `enable_send` tinyint(1) DEFAULT '0',
  `send_days` date DEFAULT NULL,
  `send_time` int(10) unsigned DEFAULT '0',
  `expires` date DEFAULT NULL,
  `timezone` int(11) DEFAULT '8',
  `keep_image` tinyint(1) DEFAULT '0',
  `level` int(1) unsigned DEFAULT '0',
  `login_time` datetime DEFAULT NULL,
  PRIMARY KEY (`k_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kinuser`
--

LOCK TABLES `kinuser` WRITE;
/*!40000 ALTER TABLE `kinuser` DISABLE KEYS */;
INSERT INTO `kinuser` VALUES (1,'zzh','3fde6bb0541387e4ebdadf7c2ff31123','zzh123@126.com',1,NULL,17,NULL,-8,0,3,'2014-03-01 15:18:49'),(2,'zz@11.com','1q2w3e',NULL,0,NULL,0,NULL,8,0,0,NULL),(3,'zz@11.comaa','4124bc0a9335c27f086f24ba207a4912',NULL,0,NULL,0,NULL,8,0,0,NULL),(4,'11','6512bd43d9caa6e02c990b0a82652dca',NULL,0,NULL,0,NULL,8,0,0,NULL),(5,'1q','852301e1234000e61546c131345e8b8a','qqqq',0,NULL,0,NULL,8,0,0,NULL),(6,'zz@11.com','1q2w3e',NULL,0,NULL,0,NULL,8,0,0,NULL),(7,'qq','2327286446091a9cab0ecf56b7d196f4','zzh1989_14@kindle.cn',0,NULL,0,NULL,8,0,0,NULL),(8,'qqqqqqqqq','343b1c4a3ea721b2d640fc8700db0f36',NULL,0,NULL,0,NULL,8,0,0,NULL),(9,'hi@11.com','3fde6bb0541387e4ebdadf7c2ff31123',NULL,0,NULL,0,NULL,8,0,0,NULL);
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

-- Dump completed on 2014-02-28 23:26:13
