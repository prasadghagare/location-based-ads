create database lba;

use lba;


CREATE TABLE user_details (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
username varchar(50) ,
phone varchar(50) ,
password varchar(50),
emailid varchar(50),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE offer_details (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
location_x varchar(50) ,
location_y varchar(50) ,
place varchar(50) ,
item varchar(50) ,
discount varchar(50),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE user_ocr_details (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
user varchar(50) ,
item varchar(50) ,
count int ,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_offers (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
username varchar(50) ,
offer varchar(200) ,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
