CREATE DATABASE IF NOT EXISTS ZoomFront;
USE ZoomFront;

CREATE TABLE IF NOT EXISTS Users(
	id serial ,
	Username varchar(255) NOT NULL UNIQUE,
	Pass varchar(255) NOT NULL,
    Balance decimal DEFAULT 0.0,
	Administrator bit DEFAULT 0,
    PRIMARY KEY (id)
);
/* Does not support rejecting friend requests. Who doesnt want more friends? */ 

CREATE TABLE IF NOT EXISTS Friends(
	id serial,
	UserID BIGINT UNSIGNED,
    FriendID BIGINT UNSIGNED,
	PRIMARY KEY(id),
    FOREIGN KEY (UserID) REFERENCES Users(id),
    FOREIGN KEY (FriendID) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Games(
	id serial,
    Title varchar(255) NOT NULL UNIQUE,
    Price decimal NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS UserLibraries(
	id serial,
	GameID BIGINT UNSIGNED,
    UserID BIGINT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY (GameID) REFERENCES Games(id),
    FOREIGN KEY (UserID) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Reviews(
	id serial,
	GameID BIGINT UNSIGNED,
    AuthorID BIGINT UNSIGNED,
    Body mediumtext,
    Rating int CHECK (Rating >= 1 AND Rating <= 5),
    PRIMARY KEY(id),
    FOREIGN KEY(AuthorID) REFERENCES Users(id),
    FOREIGN KEY(GameID) REFERENCES Games(id)
);

CREATE TABLE IF NOT EXISTS Tags(
	id serial,
    TagName varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS TagRelations(
	id serial,
	TagID BIGINT UNSIGNED,
    GameID BIGINT UNSIGNED,
    PRIMARY KEY(id),
    FOREIGN KEY (GameID) REFERENCES Games(id),
    FOREIGN KEY (TagID) REFERENCES Tags(id)
);








	
	
