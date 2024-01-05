#! /usr/bin/env python


from flask import Blueprint, render_template, session, request, redirect, url_for
from . import interfacer, loginManager, userManager, tagManager, gameManager

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == "POST":
        viewerID = int(request.form.get('viewerID',''))
        if(session['userID'] == viewerID):
            friendID = int(request.form.get('friendID',''))
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
        userFriends = userManager.getFriendsOf(session['userID'])
        friendIDs = userManager.getFriendIDs(userFriends)
        return render_template("users.html", users=userList, friendIDs = friendIDs)
    return render_template("users.html", users=userList)

@views.route('/games')
def games():
    gameList = gameManager.getAllGames()
    return render_template("games.html", games = gameList)

@views.route('/users/<int:userID>', methods=['GET','POST'])
def profile(userID):
    # Fetch userInfo
    userID = int(userID)
    userInfo = interfacer.getFromID('Users',userID)
    userLibrary = userManager.getLibrary(userID)
    userFriends = userManager.getFriendsOf(userID)


    if( request.method == "POST"):
        match (request.form.get('subType')):
            case 'addFriend':
                friendID = userID
                viewerID = session['userID']
                if( userManager.addFriend(friendID,viewerID) ):
                    print("Successfully added friend.")
                else:
                    print("Failed to add friend.")
                return redirect(url_for('users.{{userID}}'))
        
            case 'removeFriend':
                friendID = userID
                viewerID = session['userID']
                if ( userManager.deleteFriend(friendID,viewerID) ):
                    print("Sucessfully removed friend.")
                else:
                    print("Failed to remove friend.")
                return redirect(f'users.{userID}')
                return redirect(url_for('users/{{userID}}'))
            case 'balanceChange':
                # This function would obviously need input sanitation
                # in a real production environment. But thats not the goal
                # of the project. 
                balanceChange = float(request.form.get('balanceChange','0.0'))
                print("Attempting to change balance.")
                if balanceChange <= 0:
                    print("Invalid amount passed for balance change")
                else:
                    userManager.changeFunds(userID,balanceChange)
                return redirect(url_for('users.{{userID}}'))

    if(session['userID']):
        # If the VIEWER is logged in we can get their friends.
        viewerFriends = userManager.getFriendsOf(session['userID'])
        viewerFriendIDs = userManager.getFriendIDs(viewerFriends)
        return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends, friendIDs = viewerFriendIDs)

    return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends)

@views.route('/games/<int:gameID>')
def gamePage(gameID):
    gameInfo = interfacer.getFromID('Games',gameID)
    sharedTag = gameManager.getGamesWithSharedTag(gameInfo[1])

    return render_template("gamePage.html", game = gameInfo, relatedGames = sharedTag)


