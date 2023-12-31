CREATE DATABASE IF NOT EXISTS ZoomFront;
USE ZoomFront;

CREATE TABLE IF NOT EXISTS Users(
	id int NOT NULL AUTO_INCREMENT ,
    Administrator bit DEFAULT 0,
    Balance decimal DEFAULT 0.0,
    Username varchar(255) NOT NULL UNIQUE,
    Pas varchar(255) NOT NULL,

    PRIMARY KEY (id)
);
/* Does not support rejecting friend requests. Who doesnt want more friends? */ 

CREATE TABLE IF NOT EXISTS Friends(
	UserID int,
    FriendID int,
    
    PRIMARY KEY(UserID,FriendID),
    KEY(FriendID, UserID),
    FOREIGN KEY (UserID) REFERENCES Users(id),
    FOREIGN KEY (FriendID) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Games(
	id int,
    Title varchar(255) NOT NULL,
    Price decimal NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS UserLibraries(
	GameID int,
    UserID int,
    PRIMARY KEY(GameID,UserID),
    KEY(UserID,GameID),
    FOREIGN KEY (GameID) REFERENCES Games(id),
    FOREIGN KEY (UserID) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Reviews(
	id int,
    AuthorID int,
    GameID int,
    Body mediumtext,
    Rating int CHECK (Rating >= 1 AND Rating <= 5),
    PRIMARY KEY(id),
    FOREIGN KEY(AuthorID) REFERENCES Users(id),
    FOREIGN KEY(GameID) REFERENCES Games(id)
);

CREATE TABLE IF NOT EXISTS Tags(
	id int,
    TagName varchar(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS TagRelations(
	TagID int,
    GameID int,
    PRIMARY KEY(TagID, GameID),
    KEY(GameID, TagID),
    FOREIGN KEY (GameID) REFERENCES Games(id),
    FOREIGN KEY (TagID) REFERENCES Tags(id)
);
