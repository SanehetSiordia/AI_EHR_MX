-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: copy_enfermedades
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `coagulaciones`
--

DROP TABLE IF EXISTS `coagulaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coagulaciones` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `coagulaciones_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coagulaciones`
--

LOCK TABLES `coagulaciones` WRITE;
/*!40000 ALTER TABLE `coagulaciones` DISABLE KEYS */;
INSERT INTO `coagulaciones` VALUES ();
/*!40000 ALTER TABLE `coagulaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drogas_terapeuticas`
--

DROP TABLE IF EXISTS `drogas_terapeuticas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drogas_terapeuticas` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `drogas_terapeuticas_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drogas_terapeuticas`
--

LOCK TABLES `drogas_terapeuticas` WRITE;
/*!40000 ALTER TABLE `drogas_terapeuticas` DISABLE KEYS */;
INSERT INTO `drogas_terapeuticas` VALUES ();
/*!40000 ALTER TABLE `drogas_terapeuticas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hematologia`
--

DROP TABLE IF EXISTS `hematologia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hematologia` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `hematologia_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hematologia`
--

LOCK TABLES `hematologia` WRITE;
/*!40000 ALTER TABLE `hematologia` DISABLE KEYS */;
INSERT INTO `hematologia` VALUES ();
/*!40000 ALTER TABLE `hematologia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inmuno_infecto`
--

DROP TABLE IF EXISTS `inmuno_infecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inmuno_infecto` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `inmuno_infecto_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inmuno_infecto`
--

LOCK TABLES `inmuno_infecto` WRITE;
/*!40000 ALTER TABLE `inmuno_infecto` DISABLE KEYS */;
INSERT INTO `inmuno_infecto` VALUES ();
/*!40000 ALTER TABLE `inmuno_infecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inmunologia`
--

DROP TABLE IF EXISTS `inmunologia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inmunologia` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `inmunologia_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inmunologia`
--

LOCK TABLES `inmunologia` WRITE;
/*!40000 ALTER TABLE `inmunologia` DISABLE KEYS */;
INSERT INTO `inmunologia` VALUES ();
/*!40000 ALTER TABLE `inmunologia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laboratorio`
--

DROP TABLE IF EXISTS `laboratorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboratorio` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `fecha_orden` date DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `servicio_solicita` char(250) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`),
  CONSTRAINT `laboratorio_ibfk_1` FOREIGN KEY (`nss`) REFERENCES `nota_inicial` (`nss`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboratorio`
--

LOCK TABLES `laboratorio` WRITE;
/*!40000 ALTER TABLE `laboratorio` DISABLE KEYS */;
INSERT INTO `laboratorio` VALUES ();
/*!40000 ALTER TABLE `laboratorio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicina_nuclear`
--

DROP TABLE IF EXISTS `medicina_nuclear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicina_nuclear` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `medicina_nuclear_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicina_nuclear`
--

LOCK TABLES `medicina_nuclear` WRITE;
/*!40000 ALTER TABLE `medicina_nuclear` DISABLE KEYS */;
INSERT INTO `medicina_nuclear` VALUES ();
/*!40000 ALTER TABLE `medicina_nuclear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nota_egreso`
--

DROP TABLE IF EXISTS `nota_egreso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nota_egreso` (
  `nss` double NOT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `fecha_egreso` date NOT NULL,
  `especialidad_egreso` varchar(500) DEFAULT NULL,
  `motivo_egreso` varchar(500) DEFAULT NULL,
  `envio` varchar(250) DEFAULT NULL,
  `diagnostico_ingreso` varchar(800) DEFAULT NULL,
  `diagnostico_egreso` varchar(800) DEFAULT NULL,
  `resumen_evolucion` text,
  `problemas_pendientes` text,
  `plan_tratamiento` text,
  `recomendaciones` varchar(500) DEFAULT NULL,
  `factores_riesgo` varchar(500) DEFAULT NULL,
  `pronostico` varchar(500) DEFAULT NULL,
  `diagnostico_defuncion` varchar(500) DEFAULT NULL,
  `estado_salud` varchar(50) DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `talla` float DEFAULT NULL,
  `temperatura` float DEFAULT NULL,
  `frec_respiratoria` float DEFAULT NULL,
  `frec_cardiaca` float DEFAULT NULL,
  `pres_arterial` varchar(10) DEFAULT NULL,
  `imc` float DEFAULT NULL,
  `saturacion` float DEFAULT NULL,
  `glc_capilar` float DEFAULT NULL,
  `diagnostico_final` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`nss`,`fecha_egreso`),
  CONSTRAINT `nota_egreso_ibfk_1` FOREIGN KEY (`nss`) REFERENCES `nota_inicial` (`nss`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_egreso`
--

LOCK TABLES `nota_egreso` WRITE;
/*!40000 ALTER TABLE `nota_egreso` DISABLE KEYS */;
INSERT INTO `nota_egreso` VALUES ();
/*!40000 ALTER TABLE `nota_egreso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nota_inicial`
--

DROP TABLE IF EXISTS `nota_inicial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nota_inicial` (
  `nss` double NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `genero` varchar(5) DEFAULT NULL,
  `especialidad_ingreso` varchar(500) DEFAULT NULL,
  `motivo_inter` char(250) DEFAULT NULL,
  `interrogatorio` text,
  `dx` varchar(500) DEFAULT NULL,
  `plan_tratamiento` text,
  `pronostico` varchar(1000) DEFAULT NULL,
  `indicaciones` text,
  `estado_salud` varchar(50) DEFAULT NULL,
  `peso` float DEFAULT NULL,
  `talla` float DEFAULT NULL,
  `temperatura` float DEFAULT NULL,
  `frec_respiratoria` float DEFAULT NULL,
  `frec_cardiaca` float DEFAULT NULL,
  `pres_arterial` varchar(10) DEFAULT NULL,
  `imc` float DEFAULT NULL,
  `saturacion` float DEFAULT NULL,
  `glc_capilar` float DEFAULT NULL,
  `diagnostico_inicial` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`nss`,`fecha_ingreso`),
  CONSTRAINT `nota_inicial_ibfk_1` FOREIGN KEY (`nss`) REFERENCES `paciente` (`nss`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota_inicial`
--

LOCK TABLES `nota_inicial` WRITE;
/*!40000 ALTER TABLE `nota_inicial` DISABLE KEYS */;
INSERT INTO `nota_inicial` VALUES ();
/*!40000 ALTER TABLE `nota_inicial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `nss` double NOT NULL,
  PRIMARY KEY (`nss`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paciente`
--

LOCK TABLES `paciente` WRITE;
/*!40000 ALTER TABLE `paciente` DISABLE KEYS */;
INSERT INTO `paciente` VALUES ();
/*!40000 ALTER TABLE `paciente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pruebas_especiales`
--

DROP TABLE IF EXISTS `pruebas_especiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pruebas_especiales` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `pruebas_especiales_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pruebas_especiales`
--

LOCK TABLES `pruebas_especiales` WRITE;
/*!40000 ALTER TABLE `pruebas_especiales` DISABLE KEYS */;
INSERT INTO `pruebas_especiales` VALUES ();
/*!40000 ALTER TABLE `pruebas_especiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quimica_clinica`
--

DROP TABLE IF EXISTS `quimica_clinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quimica_clinica` (
  `nss` double NOT NULL,
  `folio_orden` double NOT NULL,
  `determinacion` varchar(100) NOT NULL,
  `resultado` varchar(100) DEFAULT NULL,
  `unidad` varchar(100) DEFAULT NULL,
  `valor_normal` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`nss`,`folio_orden`,`determinacion`),
  CONSTRAINT `quimica_clinica_ibfk_1` FOREIGN KEY (`nss`, `folio_orden`) REFERENCES `laboratorio` (`nss`, `folio_orden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quimica_clinica`
--

LOCK TABLES `quimica_clinica` WRITE;
/*!40000 ALTER TABLE `quimica_clinica` DISABLE KEYS */;
INSERT INTO `quimica_clinica` VALUES ();
/*!40000 ALTER TABLE `quimica_clinica` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-19  8:56:24
