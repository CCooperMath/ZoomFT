#! /usr/bin/env python 
from collections.abc import ByteString
import csv 
from . import constants as const
from .datatypes import User, Game, Tag
from .managers import UserManager, LoginManager, GameManager, TagManager

from .interfacing import Interfacer 
import random 

def generateData():

    
    config = { 
        'host' : ,
        'port' : ,
        'user' : ,
        'password' : ,
        'database' : 'ZoomFront' 
    }
    interfacer = Interfacer(config)
    userManager = UserManager(interfacer)
    loginManager = LoginManager(interfacer)
    gameManager = GameManager(interfacer)
    tagManager = TagManager(interfacer)

    # Generates fake users, and game titles / prices and populates the database
    with open('./website/FakeInfo/FakeUsers.csv', newline='') as userCSV:
        usernames = set() 
        userReader = csv.reader(userCSV)
        for row in userReader:
            loginManager.createAccount(str(row[0]),str(row[1]), float(row[2]), int(row[3]))
            usernames.add(str(row[0]))

    # Generates fake friendships between users. Adds up to 5 friendships to each assuming
    # no user tries to add themselves as a friend and isnt duplicated. 

    userList = list(usernames)
    for user in usernames:
        for i in range(0,5):
            newFriend = random.choice(userList)
            if newFriend != user:
                userManager.addFriendFromNames(user,newFriend)


    # Generates fake games. 
    with open('./website/FakeInfo/FakeGames.csv', newline='')  as gameCSV:
        gameReader = csv.reader(gameCSV)
        gameNames = set()
        for row in gameReader:
            gameManager.createGame(str(row[0]),float(row[1]))
            gameNames.add(str(row[0]))

    # Generates a tag list.
    with open('./website/FakeInfo/Tags.csv', newline='') as tagCSV:
        tagReader = csv.reader(tagCSV)
        tags = set()
        for row in tagReader:
            tagManager.createTag(str(row[0]))
            tags.add(str(row[0]))

    # Randomly adds tags to games. Adds 10 tags to each game. 
    gameList = list(gameNames)
    tagList = list(tags)
    for games in gameNames:
        for i in range(0,10):
            newTag = random.choice(tagList)
            gameManager.addTag(games,newTag)

    # Randomly add games to user libraries. Adds up to 8 games to each user. 
    for user in userList:
        for i in range(0,8):
            newGame = random.choice(gameList)
            userManager.addToLibraryFromNames(user,newGame)

    interfacer.commit()

