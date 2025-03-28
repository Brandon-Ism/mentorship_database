CREATE DATABASE IF NOT EXISTS mentorship_db;
USE mentorship_db;


-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: mentorship_db
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
-- Table structure for table `research_interests`
--

DROP TABLE IF EXISTS `research_interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `research_interests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `research_interests`
--

LOCK TABLES `research_interests` WRITE;
/*!40000 ALTER TABLE `research_interests` DISABLE KEYS */;
INSERT INTO `research_interests` VALUES (24,'Agile methodologies'),(39,'Algebra'),(1,'Algorithm design and analysis'),(9,'Anomaly detection'),(43,'Applied Mathematics'),(3,'Approximation algorithms'),(65,'ARIMA models'),(14,'Augmented and virtual reality'),(35,'Autonomous robots'),(48,'Bayesian inference'),(68,'Bayesian networks'),(90,'Biomathematics'),(89,'Biomathematics, Geometric Data Analysis'),(82,'Biomechanics'),(75,'Black holes and singularities'),(21,'Blockchain technology'),(71,'Bootstrapping'),(88,'Cellular automata'),(26,'Cloud computing'),(64,'Cluster analysis'),(56,'Combinatorial optimization'),(34,'Computability theory'),(2,'Computational complexity theory'),(10,'Computer vision'),(77,'Condensed matter physics'),(22,'Cybersecurity'),(76,'Dark matter and dark energy'),(31,'Data centers'),(16,'Data mining'),(19,'Data visualization'),(8,'Databases'),(17,'Deep learning'),(44,'Differential equations'),(27,'Distributed algorithms'),(11,'Explainable AI'),(85,'Field theory'),(57,'Financial modeling'),(84,'Fluid dynamics'),(33,'Formal languages and automata'),(83,'Fusion research'),(53,'General relativity'),(91,'Geometric Data Analysis'),(41,'Geometry'),(55,'Graph theory'),(60,'High-performance computing'),(50,'Hypothesis testing'),(62,'Inferential statistics'),(29,'Internet of Things (IoT)'),(15,'Machine learning'),(67,'Markov Chain Monte Carlo (MCMC)'),(42,'Mathematical logic'),(46,'Mathematical modeling'),(80,'Molecular biophysics'),(70,'Monte Carlo simulations'),(63,'Multivariate regression'),(7,'Natural language processing (NLP)'),(30,'Network protocols'),(54,'Nonlinear dynamics and chaos theory'),(38,'Number theory'),(45,'Numerical analysis'),(32,'Operating systems'),(47,'Optimization'),(28,'Parallel computing'),(79,'Photonic and magnetic materials'),(18,'Predictive analytics'),(66,'Predictive modeling'),(81,'Protein folding'),(20,'Public-key cryptography'),(37,'Pure Mathematics'),(86,'Quantum computing'),(73,'Quantum field theory'),(52,'Quantum mechanics'),(69,'Random sampling methods'),(6,'Reinforcement learning'),(58,'Risk management'),(36,'Robotic perception and motion planning'),(61,'Scientific computing'),(23,'Software development life cycle'),(25,'Software testing and verification'),(87,'Sports medicine'),(72,'Statistical modeling'),(59,'Stochastic calculus'),(49,'Stochastic processes'),(74,'String theory'),(78,'Superconductivity'),(4,'Supervised learning'),(51,'Time series analysis'),(40,'Topology'),(5,'Unsupervised learning'),(13,'Usability studies'),(12,'User interface design');
/*!40000 ALTER TABLE `research_interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_links`
--

DROP TABLE IF EXISTS `user_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_links` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `link` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_links_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_links`
--

LOCK TABLES `user_links` WRITE;
/*!40000 ALTER TABLE `user_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_research_interests`
--

DROP TABLE IF EXISTS `user_research_interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_research_interests` (
  `user_id` int DEFAULT NULL,
  `interest_id` int DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `interest_id` (`interest_id`),
  CONSTRAINT `user_research_interests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_research_interests_ibfk_2` FOREIGN KEY (`interest_id`) REFERENCES `research_interests` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_research_interests`
--

LOCK TABLES `user_research_interests` WRITE;
/*!40000 ALTER TABLE `user_research_interests` DISABLE KEYS */;
INSERT INTO `user_research_interests` VALUES (1,60),(1,50),(1,29),(1,15),(1,87),(2,26),(2,77),(2,11),(2,85),(2,57),(3,39),(3,1),(3,9),(5,54),(5,88),(8,89),(8,43),(8,1),(8,34),(10,57),(10,30),(10,26);
/*!40000 ALTER TABLE `user_research_interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `academic_position` enum('Undergraduate','Graduate Student','Postdoc','Faculty','Industry','Other') NOT NULL,
  `institution` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `bio` text,
  `interested_in` set('Collaboration','Providing Mentorship','Receiving Mentorship','N/A') NOT NULL,
  `headshot_path` varchar(255) DEFAULT 'static/uploads/default.jpg',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Matty Matador','matty@fake.csun.edu','Faculty','California State University, Northridge','Office of the President','Hello! I am Matty the Matador and I am looking for no collaboration at the moment!!','N/A','static/uploads/Matty-e1678816390439-circle.jpg'),(2,'Olivia Contreras','boot_with_the_fur@gmail.com','Undergraduate','CSUN','Dept. of CS','Hello!!\r\nI like cats! ','Receiving Mentorship','static/uploads/Matty-e1678816390439-circle.jpg'),(3,'John Doe','johndoe@email.com','Postdoc','University of College','Department of College','Hello','Collaboration','static/uploads/octocat-1738731809418.png'),(4,'Jane Doe','janedoe@email.com','Postdoc','Un','','','N/A','static/uploads/default.png'),(5,'test 2','test2@email.com','Graduate Student','University of College','Department of College','I am a person looking to mentor','Providing Mentorship','static/uploads/default.png'),(7,'test4','me@emaik','Undergraduate','','','','N/A','static/uploads/default.jpg'),(8,'test_update','testupdate@email.com','Postdoc','University of College','Department of College','Hello...','Providing Mentorship','static/uploads/default.jpg'),(10,'test A','test_a@email.com','Undergraduate','University of College','Department of College','hi...','Providing Mentorship','static/uploads/default.jpg');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-28  1:43:16
