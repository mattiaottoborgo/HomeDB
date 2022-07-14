SET storage_engine=INNODB;
SET FOREIGN_KEY_CHECKS=1;
CREATE DATABASE IF NOT EXISTS HomeDB;
USE HomeDB;
DROP TABLE IF EXISTS OBJECTS;
DROP TABLE IF EXISTS INSIDE;
DROP TABLE IF EXISTS BOXES;
DROP TABLE IF EXISTS ROOM;

CREATE TABLE OBJECTS(
ObjectId VARCHAR(50),
ObjectName VARCHAR(50) NOT NULL,
PAthImage VARCHAR (100),
PRIMARY KEY(ObjectId)
);

CREATE TABLE ROOM(
    RoomID VARCHAR(50),
    RoomName VARCHAr(50),
    PRIMARY KEY(RoomID)
);



CREATE TABLE BOXES(
BoxId VARCHAR (50),
BoxNumber SMALLINT,
RoomID VARCHAR(50),
PRIMARY KEY (BoxId),
FOREIGN KEY(RoomID) REFERENCES ROOM(RoomID) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE INSIDE(
    ObjectId VARCHAR(50),
    BoxId VARCHAR(50),
    RoomID VARCHAR(50),
    FOREIGN KEY (ObjectId) REFERENCES OBJECTS(ObjectId)  ON DELETE SET NULL ON UPDATE CASCADE ,
    FOREIGN KEY (BoxId) REFERENCES BOXES(BoxId) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES ROOM(RoomID) ON DELETE SET NULL ON UPDATE CASCADE
);