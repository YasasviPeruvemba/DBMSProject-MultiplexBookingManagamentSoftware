create database project;

use project;

CREATE TABLE `login` (
  `Password` varchar(30) NOT NULL,
  `Username` varchar(30) NOT NULL,
  PRIMARY KEY (`Username`)
);

CREATE TABLE `customer` (
  `Username` varchar(30) NOT NULL,
  `Password` varchar(30) NOT NULL,
  `First_Name` varchar(20) DEFAULT NULL,
  `Last_Name` varchar(20) DEFAULT NULL,
  `Gender` varchar(2) DEFAULT NULL,
  `Phone` varchar(11) DEFAULT NULL,
  `Mail` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Username`,`Password`)
);

CREATE TABLE `movies` (
  `Mov_Name` varchar(30) NOT NULL,
  `Genre` varchar(50) DEFAULT NULL,
  `Rating` decimal(3,1) DEFAULT NULL,
  `COST` int(5) DEFAULT NULL,
  PRIMARY KEY (`Mov_Name`)
);

CREATE TABLE `multiplex` (
  `MULTIPLEX_ID` int(11) NOT NULL AUTO_INCREMENT,
  `MULTIPLEX_NAME` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`MULTIPLEX_ID`)
);

CREATE TABLE `shows` (
  `SHOW_ID` int(11) NOT NULL AUTO_INCREMENT,
  `MOV_NAME` varchar(30) NOT NULL,
  `MULTIPLEX_ID` int(11) NOT NULL,
  `HALL_NO` varchar(5) DEFAULT NULL,
  `DATE` date DEFAULT NULL,
  `TIMING` time DEFAULT NULL,
  PRIMARY KEY (`SHOW_ID`,`MOV_NAME`,`MULTIPLEX_ID`)
);

CREATE TABLE `coupon` (
  `COUPON_ID` varchar(15) DEFAULT NULL,
  `DISCOUNT` int(3) DEFAULT NULL,
  `STATUS` bit(1) DEFAULT NULL
);

CREATE TABLE `tickets` (
  `T_ID` int(11) NOT NULL AUTO_INCREMENT,
  `SEAT_NO` int(3) DEFAULT NULL,
  `USERNAME` varchar(30) DEFAULT NULL,
  `SHOW_ID` int(11) DEFAULT NULL,
  `COST` int(11) DEFAULT NULL,
  PRIMARY KEY (`T_ID`)
);

CREATE TABLE `feedback` (
  `Message` text,
  `Date` date DEFAULT NULL,
  `Username` varchar(30) DEFAULT NULL
);

CREATE TABLE `billing` (
  `T_ID` int(11) NOT NULL,
  `USERNAME` varchar(30) NOT NULL,
  `PURCH_AMT` int(11) DEFAULT NULL,
  `DATE_OF_PURCHASE` date DEFAULT NULL,
  `Multiplex_name` varchar(30) DEFAULT NULL
);

insert into movies values("Inception","Action/Thriller",4.8);
insert into movies values("The Dark Knight","Crime/Thriller",4.4);
insert into movies values("Interstellar","Sci-Fi",4.9);
insert into movies values("Dunkirk","Drama/Thriller",4.2);

-- TRIGGERS

DELIMITER //;
CREATE TRIGGER `BILL` AFTER INSERT ON `tickets` 
FOR EACH ROW 
BEGIN
INSERT INTO BILLING VALUES(NEW.T_ID,NEW.USERNAME,NEW.COST,NOW(),(SELECT MULTIPLEX_NAME FROM MULTIPLEX,SHOWS WHERE MULTIPLEX.MULTIPLEX_ID=SHOWS.MULTIPLEX_ID AND SHOW_ID=NEW.SHOW_ID));
DELIMITER ;

DELIMITER //
CREATE TRIGGER `REMOVESHOWS` AFTER DELETE ON `movies` 
FOR EACH ROW 
BEGIN
DELETE FROM SHOWS WHERE MOV_NAME=OLD.MOV_NAME;
DELIMITER ;

-- PROCEDURE

CREATE PROCEDURE `DELETEMOVIE`(IN MOVIENAME VARCHAR(30))
BEGIN
DELETE FROM MOVIES WHERE MOV_NAME=MOVIENAME;