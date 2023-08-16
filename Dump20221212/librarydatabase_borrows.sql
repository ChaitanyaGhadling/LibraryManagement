-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: librarydatabase
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `borrows`
--

DROP TABLE IF EXISTS `borrows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrows` (
  `bor_no` int NOT NULL,
  `docid` int NOT NULL,
  `copyno` int NOT NULL,
  `bid` int NOT NULL,
  `rid` int DEFAULT NULL,
  PRIMARY KEY (`bor_no`,`bid`,`copyno`,`docid`),
  KEY `b_copy_idx` (`docid`,`copyno`,`bid`),
  KEY `b_rid_idx` (`rid`),
  CONSTRAINT `b_copy` FOREIGN KEY (`docid`, `copyno`, `bid`) REFERENCES `copy` (`docid`, `copyno`, `bid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `b_rid` FOREIGN KEY (`rid`) REFERENCES `reader` (`rid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `bor_no` FOREIGN KEY (`bor_no`) REFERENCES `borrowing` (`bor_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrows`
--

LOCK TABLES `borrows` WRITE;
/*!40000 ALTER TABLE `borrows` DISABLE KEYS */;
INSERT INTO `borrows` VALUES (251,21,1001,51,71),(262,21,1002,51,72),(263,21,1003,51,72),(253,23,1003,53,73),(254,24,1004,54,74),(256,26,1006,56,76),(257,27,1007,57,77),(258,28,1008,58,78),(259,29,1009,59,79),(260,30,1010,60,80),(261,31,1011,61,81);
/*!40000 ALTER TABLE `borrows` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-12 17:16:14
