#! /usr/bin/env python


from flask import Blueprint, render_template
from . import interfacer, loginManager, userManager, tagManager, gameManager

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/users')
def user():
    userList = userManager.getAllUsers()
    print(userList)
    return render_template("users.html", users = userList)

@views.route('/games')
def games():
    gameList = gameManager.getAllGames()
    return render_template("games.html", games = gameList)

@views.route('/users/<int:userID>')
def profile(userID):
    # Fetch userInfo 
    userInfo = interfacer.getFromID('Users',userID)

    username = userInfo[1]
    userLibrary = userManager.getLibrary(username)
    userFriends = userManager.getFriendsOf(username)
    print(userLibrary)
    print(userFriends)
    return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends)

@views.route('/games/<int:gameID>')
def gamePage(gameID):
    gameInfo = interfacer.getFromID('Games',gameID)
    sharedTag = gameManager.getGamesWithSharedTag(gameInfo[1])
    print(sharedTag)
    return render_template("gamePage.html", game = gameInfo, relatedGames = sharedTag)


