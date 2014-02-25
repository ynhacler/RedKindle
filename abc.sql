-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: redkindle
-- ------------------------------------------------------
-- Server version	5.5.35-0+wheezy1

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
) ENGINE=MyISAM AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds`
--

LOCK TABLES `feeds` WRITE;
/*!40000 ALTER TABLE `feeds` DISABLE KEYS */;
INSERT INTO `feeds` VALUES (35,'三联生活周刊','http://app.lifeweek.com.cn/?app=rss&controller=index&action=feed',0),(24,'知乎每日精选','http://www.zhihu.com/rss',0),(25,'BBC中文网','http://www.bbc.co.uk/zhongwen/simp/index.xml',0),(26,'果壳网','http://www.guokr.com/rss/',0),(27,'FT中文网_英国《金融时报》(Financial Times)','http://www.ftchinese.com/rss/feed',0),(28,'科学松鼠会','http://songshuhui.net/feed',1),(29,'读经典','http://17dujingdian.com/rss',1),(30,'纽约时报中文网','http://cn.nytimes.com/rss.html',1),(31,'Engadget 中国版','http://cn.engadget.com/rss.xml',1),(32,'36氪','http://feed.36kr.com/c/33346/f/566026/index.rss',0),(33,'豆瓣最受欢迎的书评','DoubanBook',0),(34,'知乎日报','ZhihuDaily',0),(36,'华尔街见闻','http://wallstreetcn.com/feed',0),(37,'左岸读书','http://feed.feedsky.com/clzzxf',1),(38,'PingWest','http://www.pingwest.com/feed/',1),(39,'虎嗅网','http://www.huxiu.com/rss/0.xml',0),(40,'爱范儿 · Beats of Bits','http://www.ifanr.com/feed',1),(41,'HackerNews','https://news.ycombinator.com/rss',0),(42,'墙外楼','http://feeds.feedburner.com/letscorp/aDmw',1),(43,'一个-韩寒','http://caodan.org/feed',1);
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
) ENGINE=MyISAM AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeds_user`
--

LOCK TABLES `feeds_user` WRITE;
/*!40000 ALTER TABLE `feeds_user` DISABLE KEYS */;
INSERT INTO `feeds_user` VALUES (108,1,34),(63,3,26),(64,3,27),(65,3,28),(66,3,30),(68,4,24),(69,4,25),(76,6,25),(77,6,27),(79,8,24),(80,8,25),(81,8,26),(82,8,29),(83,8,33),(84,11,25),(85,11,27),(86,11,30),(87,12,24),(88,12,33);
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
  `level` int(1) unsigned DEFAULT '0',
  PRIMARY KEY (`k_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kinuser`
--

LOCK TABLES `kinuser` WRITE;
/*!40000 ALTER TABLE `kinuser` DISABLE KEYS */;
INSERT INTO `kinuser` VALUES (1,'zzh','3fde6bb0541387e4ebdadf7c2ff31123','zzh1989_14@kindle.cn',0,NULL,13,NULL,8,0,3),(2,'test','098f6bcd4621d373cade4e832627b4f6','caoshou_xin@1.com',0,NULL,0,NULL,8,0,0),(3,'admin','21232f297a57a5a743894a0e4a801fc3','zzh1989@126.com',0,NULL,0,NULL,8,0,0),(4,'ppzhoujun@gmail.com','202cb962ac59075b964b07152d234b70','ppzhoujun@gmail.com',0,NULL,0,NULL,8,0,0),(13,'szh123h@163.com','eb37e9ca05cae99c65cb5037b82ef948',NULL,0,NULL,0,NULL,8,0,0),(5,'himybear@sina.com','cf2215e08075fd1c2407245292a28420',NULL,0,NULL,0,NULL,8,0,0),(6,'shuyk1983@Gmail. com','a66301c5f25c763ec87e1e2bec0a5ed8','shuyk1983@kindle.com',0,NULL,0,NULL,8,0,0),(7,'winkat@vip.qq.com','b16a2f58ef5ee49097a94dc24de8580b',NULL,0,NULL,0,NULL,8,0,0),(8,'wangchenan@outlook.com','58e40052173077baefeb3edc85784352','wangchenan@kindle.cn',1,NULL,12,NULL,8,0,0),(9,'xiongxiaokun@sina.com','82f2c1f171cea50e688243570a04e6f6',NULL,0,NULL,0,NULL,8,0,0),(10,'yangtiening1983@gmail.com','270a3ce14f15b2e8db28840319bba1a8',NULL,0,NULL,0,NULL,8,0,0),(11,'qianshi1026@hotmail.com','d8ed886e10039b91d5734da6e4523520','qianshi1026@kindle.cn',1,NULL,9,NULL,8,1,0),(12,'lichaoleo@163.com','c5d554fb31d0b0944e8c3d59899112a9',NULL,0,NULL,0,NULL,8,0,0),(14,'linandblue@hotmail.com','fcbf750fc74a66517c74dd4f2fe629b2',NULL,0,NULL,0,NULL,8,0,0),(15,'Summer-zhiyan@hotmail.com','fdaf63573f9c52118ede0323b07ce2e9',NULL,0,NULL,0,NULL,8,0,0),(16,'772469017@qq.com','fdaf63573f9c52118ede0323b07ce2e9',NULL,0,NULL,0,NULL,8,0,0),(17,'zifawhy@gmail.com','02d69a696a51f24315ac502846a51ff3',NULL,0,NULL,0,NULL,8,0,0);
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

-- Dump completed on 2014-02-25 13:11:30
