-- ovw.sql
-- sql code to create the database and tables for use in the


-- Create the Database if it does not exsist yet
CREATE DATABASE IF NOT EXISTS ovw DEFAULT CHARACTER SET utf8;

USE ovw;

/*table drop order done to preserve referrential integrity*/
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS tips;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
    uID int(10) AUTO_INCREMENT,
    username varchar(30) DEFAULT NULL,
    password varchar(100) DEFAULT NULL,
    permission enum('admin','player'),
    PRIMARY KEY (uID)
) ENGINE=InnoDB;

CREATE TABLE tips (
    tipID int(10) AUTO_INCREMENT,
    title varchar(30) DEFAULT NULL,
    postText varchar(3000) DEFAULT NULL,
    uID int(10),
    image mediumblob,
    
    hero enum('Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree',
    'Mei','Pharah','Reaper','Soldier:76','Sombra','Symmetra','Torbjörn',
    'Tracer','Widowmaker','D.Va','Orisa','Reinhardt','Roadhog','Winston',
    'Wrecking Ball','Zarya','Ana','Baptiste','Bridgette','Lúcio','Mercy',
    'Moira','Zenyatta','All') DEFAULT 'All',
    
    map enum('Hanamura','Horizon Lunar Colony','Paris','Temple of Anubis',
    'Volskaya Industries','Dorado','Junkertown','Rialto','Route 66',
    'Watchpoint: Gibralter','Blizzard World','Eichenwalde','Hollywood',
    'Kings Row','Numbani','Busan','Ilios','Lijang Tower','Nepal','Oasis','All') DEFAULT 'All',
    
    difficulty enum('Beginner', 'Intermediate', 'Advanced', 'Expert') DEFAULT 'Beginner',
    datePosted datetime DEFAULT NULL,
    
    FOREIGN KEY (uID) REFERENCES user (uID) ON DELETE SET NULL ON UPDATE CASCADE,
    PRIMARY KEY (tipID)
) ENGINE=InnoDB;


/*our pirmary key is just (commentID) as opposed to (tipID,commentID) because
we cannot have a key tuple when theere is an auto_increment row */

CREATE TABLE comments(
    commentID int(10) auto_increment,
    uID int(10),
    tipID int(10),
    commentText varchar(1000),
    datePosted datetime, 
    FOREIGN KEY (tipID) REFERENCES tips(tipID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (uID) REFERENCES user(uID) ON DELETE SET NULL ON UPDATE CASCADE,
    primary key (commentID),
    key tipID (tipID),
    UNIQUE(tipID,commentID)
    )
    ENGINE = InnoDB;
    
    

CREATE TABLE likes (
  uID int(10),
  tipID int(10),
  PRIMARY KEY (uID,tipID),
  key (uID),
  key tipID (tipID),
  UNIQUE(uID,tipID),
  FOREIGN KEY (tipID) REFERENCES tips(tipID) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (uID) REFERENCES user(uID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;