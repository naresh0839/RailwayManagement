DROP DATABASE railway_management;
CREATE DATABASE IF NOT EXISTS railway_management;
USE railway_management;

-- Table structure for table `Account`

DROP TABLE IF EXISTS `Account`;
CREATE TABLE `Account` (
  `Username` varchar(15) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Email_Id` varchar(35) NOT NULL,
  `Address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Username`)
);

INSERT INTO `Account` VALUES ('shaan','buddha','shaan123rock@gmail.com','Bokaro'),('zuhair','qwerty','mdzuhair66@gmail.com','Kolkata'),('naresh','asdfgh','naresh0839@gmail.com','Sirsa Haryana'),('sayan','famislove','gsayan@gmail.com','Jabalpur');

-- Table structure for table `Contact`

DROP TABLE IF EXISTS `Contact`;
CREATE TABLE `Contact` (
  `Username` varchar(15) NOT NULL DEFAULT '',
  `Phone_No` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`Username`,`Phone_No`),
  CONSTRAINT `Contact_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `Account` (`Username`) ON DELETE CASCADE
); 

INSERT INTO `Contact` VALUES ('shaan','1234567899'),('naresh','7289809959'),('zuhair','1234567899'),('sayan','1234567899'); 

-- Table structure for table `Station`

DROP TABLE IF EXISTS `Station`;
CREATE TABLE `Station` (
  `Station_Code` char(5) NOT NULL DEFAULT '',
  `Station_Name` varchar(25) NOT NULL,
  PRIMARY KEY (`Station_Code`)
);

INSERT INTO `Station` VALUES ('ALD','ALLAHABAD JUNCTION'),('CNB','KANPUR CENTRAL'),('GYN','GYANPUR ROAD'),('GZB','GHAZIABAD JUNCTION'),('MUV','MANDUADIH'),('NDLS','NEW DELHI');
INSERT INTO `Station` VALUES ('NZM','H NIZAMUDDIN'),('BVH','BALLABGARH'),('MTJ','MATHURA JN'),('BTE','BHARATPUR JN'),('BXN','BAYANA JN'),('HAN','HINDAUN CITY'),('SMBJ','SHRI MAHABIRJI'),('GGC','GANGAPUR CITY'),('SWM','SAWAI MADHOPUR'),('KOTA','KOTA JN');


-- Table structure for table `Train`

DROP TABLE IF EXISTS `Train`;
CREATE TABLE `Train` (
  `Train_No` int(6) NOT NULL DEFAULT '0',
  `Name` varchar(25) NOT NULL,
  `Seat_Sleeper` int(4) NOT NULL,
  `Seat_First_Class_AC` int(4) NOT NULL,
  `Seat_Second_Class_AC` int(4) NOT NULL,
  `Seat_Third_Class_AC` int(4) NOT NULL,
  `Wifi` char(1) NOT NULL,
  `Food` char(1) NOT NULL,
  `Run_On_Sunday` char(1) NOT NULL,
  `Run_On_Monday` char(1) NOT NULL,
  `Run_On_Tuesday` char(1) NOT NULL,
  `Run_On_Wednesday` char(1) NOT NULL,
  `Run_On_Thursday` char(1) NOT NULL,
  `Run_On_Friday` char(1) NOT NULL,
  `Run_On_Saturday` char(1) NOT NULL,
  PRIMARY KEY (`Train_No`)
);

INSERT INTO `Train` VALUES (12559,'SHIV GANGA EXP',479,47,96,192,'N','Y','Y','Y','Y','Y','Y','Y','Y'),(12560,'SHIV GANGA EXP',480,43,96,192,'N','Y','Y','Y','Y','Y','Y','Y','Y'),(12581,'MUV NDLS S F EX',432,48,80,144,'N','N','Y','Y','Y','Y','Y','Y','Y'),(12582,'MUV NDLS S F EX',432,48,80,144,'N','N','Y','Y','Y','Y','Y','Y','Y');
INSERT INTO `Train` VALUES (02060,'KOTA JANSHTBDI',479,47,96,192,'N','Y','Y','Y','Y','Y','Y','Y','Y');

-- Table structure for table `Ticket`

DROP TABLE IF EXISTS `Ticket`;
CREATE TABLE `Ticket` (
  `Ticket_No` int(10) NOT NULL AUTO_INCREMENT,
  `Train_No` int(6) NOT NULL,
  `Date_of_Journey` date NOT NULL,
  `Username` varchar(15) NOT NULL,
  PRIMARY KEY (`Ticket_No`),
  KEY `Username` (`Username`),
  KEY `Train_No` (`Train_No`),
  CONSTRAINT `Ticket_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `Account` (`Username`) ON DELETE CASCADE,
  CONSTRAINT `Ticket_ibfk_2` FOREIGN KEY (`Train_No`) REFERENCES `Train` (`Train_No`) ON UPDATE CASCADE
);

-- Table structure for table `Passenger`

DROP TABLE IF EXISTS `Passenger`;
CREATE TABLE `Passenger` (
  `Passenger_Id` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(20) NOT NULL,
  `Last_Name` varchar(20) NOT NULL,
  `Gender` char(1) NOT NULL,
  `Phone_No` char(10) DEFAULT NULL,
  `Ticket_No` int(10) NOT NULL,
  `Age` int(11) NOT NULL,
  `Class` varchar(20) NOT NULL,
  PRIMARY KEY (`Passenger_Id`),
  KEY `Ticket_No` (`Ticket_No`),
  CONSTRAINT `Passenger_ibfk_1` FOREIGN KEY (`Ticket_No`) REFERENCES `Ticket` (`Ticket_No`) ON DELETE CASCADE
);

-- Table structure for table `Stoppage`

DROP TABLE IF EXISTS `Stoppage`;
CREATE TABLE `Stoppage` (
  `Train_No` int(6) NOT NULL DEFAULT '0',
  `Station_Code` char(5) NOT NULL DEFAULT '',
  `Arrival_Time` time DEFAULT NULL,
  `Departure_Time` time DEFAULT NULL,
  PRIMARY KEY (`Train_No`,`Station_Code`),
  KEY `Station_Code` (`Station_Code`),
  CONSTRAINT `Stoppage_ibfk_1` FOREIGN KEY (`Train_No`) REFERENCES `Train` (`Train_No`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Stoppage_ibfk_2` FOREIGN KEY (`Station_Code`) REFERENCES `Station` (`Station_Code`) ON DELETE CASCADE ON UPDATE CASCADE
); 

INSERT INTO `Stoppage` VALUES (12559,'ALD','22:05:00','22:30:00'),(12559,'CNB','01:30:00','01:38:00'),(12559,'MUV','19:20:00','19:30:00'),(12559,'NDLS','08:10:00',NULL),(12560,'ALD','03:45:00','04:10:00'),(12560,'CNB','01:00:00','01:05:00'),(12560,'MUV','07:00:00',NULL),(12560,'NDLS','18:35:00','18:55:00'),(12581,'ALD','01:20:00','01:45:00'),(12581,'CNB','04:15:00','04:20:00'),(12581,'GYN','23:31:00','23:33:00'),(12581,'GZB','11:30:00','11:32:00'),(12581,'MUV','22:20:00','22:30:00'),(12581,'NDLS','12:20:00',NULL),(12582,'ALD','07:45:00','08:15:00'),(12582,'CNB','04:55:00','05:00:00'),(12582,'GYN','09:21:00','09:23:00'),(12582,'GZB','23:03:00','23:05:00'),(12582,'MUV','11:20:00',NULL),(12582,'NDLS','22:15:00','22:25:00');
INSERT INTO `Stoppage` VALUES (02060,'NZM','13:15:00 ','13:15:00'),(02060,'BVH','13:38:00','13:40:00'),(02060,'MTJ','15:05:00','15:10:00'),(02060,'BTE','15:38:00','15:40:00'),(02060,'BXN','16:09:00','16:10:00'),(02060,'HAN','16:34:00','16:35:00'),(02060,'SMBJ','16:45:00','16:46:00'),(02060,'GGC','17:18:00','17:20:00'),(02060,'SWM','18:03:00','18:05:00'),(02060,'KOTA','20:00:00','20:00:00');
