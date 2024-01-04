#! /usr/bin/env python


from flask import Blueprint, render_template, session, request
from . import interfacer, loginManager, userManager, tagManager, gameManager

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == "POST":
        viewerID = int(request.form.get('viewerID'))
        if(session['userID'] == viewerID):
            friendID = int(request.form.get('friendID'))
            match request.form.get('subType'):
                case 'removeFriend':
                    success = userManager.deleteFriend(viewerID,friendID)
                    if(success):
                        print("Friend removed.")
                    else:
                        print("Failed to remove friend.")
                case 'addFriend':
                    success = userManager.addFriend(viewerID,friendID)
                    if(success):
                        print("Friend added.")
                    else:
                        print("Failed to add friend.")

        else:
            print("Session and viewerID mismatch")




    userList = userManager.getAllUsers()
    if session['userID']:
        userFriends = userManager.getFriendsOf(session['username'])
        friendIDs = userManager.getFriendIDs(userFriends)
        return render_template("users.html", users=userList, friendIDs = friendIDs)
    return render_template("users.html", users=userList)

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
    return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends)

@views.route('/games/<int:gameID>')
def gamePage(gameID):
    gameInfo = interfacer.getFromID('Games',gameID)
    sharedTag = gameManager.getGamesWithSharedTag(gameInfo[1])
    print(sharedTag)
    return render_template("gamePage.html", game = gameInfo, relatedGames = sharedTag)


