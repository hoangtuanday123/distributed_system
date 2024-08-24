-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: distributed_system
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_account_roleuser` (`role_id`),
  CONSTRAINT `fk_account_roleuser` FOREIGN KEY (`role_id`) REFERENCES `roleuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'pnhtuanhcmus@gmail.com','123456','2024-06-16',1),(4,'pnhtuanjob@gmail.com','123456','2024-06-16',2),(5,'abc@gmail.com','123456','2024-08-03',1);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calendar`
--

DROP TABLE IF EXISTS `calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calendar` (
  `id` int NOT NULL AUTO_INCREMENT,
  `checkin` datetime DEFAULT NULL,
  `checkout` datetime DEFAULT NULL,
  `idaccount` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar`
--

LOCK TABLES `calendar` WRITE;
/*!40000 ALTER TABLE `calendar` DISABLE KEYS */;
INSERT INTO `calendar` VALUES (7,'2024-06-22 10:56:58','2024-06-22 10:57:07',1),(8,'2024-06-22 10:58:46',NULL,1),(9,'2024-06-22 11:22:17','2024-06-22 11:23:56',1),(10,'2024-06-22 11:24:11',NULL,1),(11,'2024-08-03 09:35:05','2024-08-03 09:35:43',2),(12,'2024-08-03 09:35:53',NULL,3),(13,'2024-08-04 14:16:08','2024-08-04 14:17:19',2),(14,'2024-08-04 14:26:24','2024-08-04 14:29:21',2),(15,'2024-08-04 14:30:06','2024-08-04 14:30:34',1),(16,'2024-08-04 15:04:33','2024-08-04 15:17:18',2),(17,'2024-08-04 15:52:38',NULL,2),(18,'2024-08-04 16:05:02','2024-08-04 16:07:34',2),(19,'2024-08-04 16:07:51','2024-08-04 16:09:35',2),(20,'2024-08-04 16:08:26',NULL,2),(21,'2024-08-04 16:10:40',NULL,2),(22,'2024-08-04 16:12:10','2024-08-04 16:12:14',2),(23,'2024-08-04 16:12:31',NULL,2),(24,'2024-08-04 16:13:41',NULL,2),(25,'2024-08-04 16:19:12','2024-08-04 16:19:15',2),(26,'2024-08-04 16:20:10','2024-08-04 16:20:14',2),(27,'2024-08-04 16:21:33',NULL,2),(28,'2024-08-04 16:22:39',NULL,2),(29,'2024-08-04 16:23:01','2024-08-04 16:24:35',2),(30,'2024-08-04 16:35:02',NULL,2),(31,'2024-08-04 16:35:30','2024-08-04 16:35:46',2),(32,'2024-08-04 16:38:43','2024-08-04 16:38:49',2),(33,'2024-08-04 16:53:17','2024-08-04 16:53:28',2),(34,'2024-08-04 17:02:21','2024-08-04 17:02:41',2),(35,'2024-08-04 17:03:13','2024-08-04 17:03:28',2),(36,'2024-08-04 17:09:05',NULL,2),(37,'2024-08-04 17:15:06','2024-08-04 17:15:22',2),(38,'2024-08-04 17:26:04',NULL,2),(39,'2024-08-04 17:32:51',NULL,2),(40,'2024-08-04 17:37:24','2024-08-04 17:38:53',2),(41,'2024-08-04 17:40:54',NULL,1),(42,'2024-08-04 19:22:53','2024-08-04 19:30:29',2),(43,'2024-08-04 19:30:48',NULL,1),(44,'2024-08-04 21:54:52',NULL,1),(45,'2024-08-04 22:07:56',NULL,2),(46,'2024-08-04 22:32:20','2024-08-04 23:07:56',1),(47,'2024-08-13 06:55:05','2024-08-13 07:04:01',1),(48,'2024-08-13 07:04:17',NULL,2),(49,'2024-08-13 07:08:19',NULL,1),(50,'2024-08-15 20:26:23',NULL,1),(51,'2024-08-17 11:25:26',NULL,1),(52,'2024-08-17 12:54:57',NULL,1),(53,'2024-08-17 13:19:05',NULL,2),(54,'2024-08-17 13:20:44',NULL,1),(55,'2024-08-17 13:21:33',NULL,1),(56,'2024-08-17 13:23:46',NULL,1),(57,'2024-08-17 13:23:58',NULL,1),(58,'2024-08-17 13:24:30',NULL,1),(59,'2024-08-17 13:25:09',NULL,1),(60,'2024-08-17 13:27:06',NULL,1),(61,'2024-08-17 13:27:47','2024-08-17 13:28:41',1),(62,'2024-08-17 13:30:31','2024-08-17 13:30:34',1),(63,'2024-08-17 13:32:18','2024-08-17 13:32:23',1),(64,'2024-08-17 13:32:32','2024-08-17 13:32:35',1),(65,'2024-08-17 13:42:38','2024-08-17 13:43:08',1),(66,'2024-08-17 13:43:45',NULL,2),(67,'2024-08-18 11:02:04',NULL,1);
/*!40000 ALTER TABLE `calendar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_off`
--

DROP TABLE IF EXISTS `leave_off`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_off` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task` varchar(50) DEFAULT NULL,
  `projectid` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_lv_p` (`projectid`),
  CONSTRAINT `fk_lv_p` FOREIGN KEY (`projectid`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_off`
--

LOCK TABLES `leave_off` WRITE;
/*!40000 ALTER TABLE `leave_off` DISABLE KEYS */;
INSERT INTO `leave_off` VALUES (5,'Marriage',1),(6,'Child\'s marriage',1),(7,'Death of parent',1),(8,'Dayoff',1),(9,NULL,2);
/*!40000 ALTER TABLE `leave_off` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profileuser`
--

DROP TABLE IF EXISTS `profileuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profileuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) DEFAULT NULL,
  `cccd` varchar(20) DEFAULT NULL,
  `tax` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `bankcode` varchar(20) DEFAULT NULL,
  `bankname` varchar(20) DEFAULT NULL,
  `idaccount` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_profile_account` (`idaccount`),
  CONSTRAINT `fk_profile_account` FOREIGN KEY (`idaccount`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profileuser`
--

LOCK TABLES `profileuser` WRITE;
/*!40000 ALTER TABLE `profileuser` DISABLE KEYS */;
INSERT INTO `profileuser` VALUES (1,'tuan','1','1','1','1','1','1',1),(2,'tuanjob','1','1','1','1','1','1',4),(3,'hoang tuan','1','1','0843055059','hcm','1','bidv',5);
/*!40000 ALTER TABLE `profileuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `projecttype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'leave'),(2,'work from home');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roleuser`
--

DROP TABLE IF EXISTS `roleuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roleuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rolename` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roleuser`
--

LOCK TABLES `roleuser` WRITE;
/*!40000 ALTER TABLE `roleuser` DISABLE KEYS */;
INSERT INTO `roleuser` VALUES (1,'employee'),(2,'manager');
/*!40000 ALTER TABLE `roleuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timesheet`
--

DROP TABLE IF EXISTS `timesheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timesheet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `updatedate` date DEFAULT NULL,
  `hours` int DEFAULT NULL,
  `idprofile` int DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_t_profile` (`idprofile`),
  CONSTRAINT `fk_t_profile` FOREIGN KEY (`idprofile`) REFERENCES `profileuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timesheet`
--

LOCK TABLES `timesheet` WRITE;
/*!40000 ALTER TABLE `timesheet` DISABLE KEYS */;
INSERT INTO `timesheet` VALUES (13,'2024-08-07',8,1,'unapproval');
/*!40000 ALTER TABLE `timesheet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_avatar`
--

DROP TABLE IF EXISTS `user_avatar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_avatar` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idprofile` int DEFAULT NULL,
  `pic_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_avatar_prfile` (`idprofile`),
  CONSTRAINT `fk_avatar_prfile` FOREIGN KEY (`idprofile`) REFERENCES `profileuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_avatar`
--

LOCK TABLES `user_avatar` WRITE;
/*!40000 ALTER TABLE `user_avatar` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_avatar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_request`
--

DROP TABLE IF EXISTS `user_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idtask` int DEFAULT NULL,
  `idprofile` int DEFAULT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_er_task` (`idtask`),
  CONSTRAINT `fk_er_task` FOREIGN KEY (`idtask`) REFERENCES `leave_off` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_request`
--

LOCK TABLES `user_request` WRITE;
/*!40000 ALTER TABLE `user_request` DISABLE KEYS */;
INSERT INTO `user_request` VALUES (6,5,1,'2024-08-15','2024-08-16','marige','unapproval'),(7,9,1,'2024-08-21','2024-08-24','wfh','unapproval'),(9,5,1,'2024-08-17','2024-08-18','cfffff','unapproval'),(10,5,1,'2024-08-22','2024-08-21','ssss','created');
/*!40000 ALTER TABLE `user_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wft`
--

DROP TABLE IF EXISTS `wft`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wft` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idprofile` int DEFAULT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wft`
--

LOCK TABLES `wft` WRITE;
/*!40000 ALTER TABLE `wft` DISABLE KEYS */;
/*!40000 ALTER TABLE `wft` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-20 20:58:17
