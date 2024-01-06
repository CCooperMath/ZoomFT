#! /usr/bin/env python


from flask import Blueprint, render_template, session, request, redirect, url_for
from . import interfacer, loginManager, userManager, tagManager, gameManager
from . import constants as const
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
    if(session['userID']):
        # A user is signed in. We can check their library. 
        userLibrary = userManager.getLibrary(session['userID'])
        libraryIDs = {game[1] for game in userLibrary}
        return render_template("games.html", games = gameList, libraryIDs = libraryIDs)
    else:   
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
        
                return redirect(f'/users/{userID}')
            case 'removeFriend':
                friendID = userID
                viewerID = session['userID']
                if ( userManager.deleteFriend(friendID,viewerID) ):
                    print("Sucessfully removed friend.")
                else:
                    print("Failed to remove friend.")
                return redirect(f'/users/{userID}')
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
                    session['accountBalance'] = interfacer.getFromID('Users',userID)[const.SQL_BALANCE]

                return redirect(f'/users/{userID}')

    if(session['userID']):
        # If the VIEWER is logged in we can get their friends.
        viewerFriends = userManager.getFriendsOf(session['userID'])
        viewerFriendIDs = userManager.getFriendIDs(viewerFriends)
        return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends, friendIDs = viewerFriendIDs)

    return render_template("profile.html", userInfo = userInfo, library = userLibrary, 
                           friends = userFriends)

@views.route('/games/<int:gameID>', methods=['GET','POST'])
def gamePage(gameID):
    gameInfo = interfacer.getFromID('Games',gameID)
    if(gameInfo != None):
        sharedTag = gameManager.getGamesWithSharedTag(gameInfo[1])
        if(request.method == 'POST'):
            match(request.form.get('subType')):
                case 'purchaseRequest':
                    print("Purchasing")
                    user = interfacer.getFromID('Users',session['userID'])
                    if user != None and gameInfo != None :
                        userBalance = float(user[const.SQL_BALANCE])
                        gamePrice  = float(gameInfo[const.SQL_PRICE])
                        if(userBalance >= gamePrice):
                            gamePrice = -gamePrice
                            userManager.changeFunds(session['userID'],gamePrice)
                            userManager.addToLibrary(session['userID'],gameID)
                    return redirect(f'/games/{gameID}')

        currentUser = interfacer.getFromID('Users',session['userID'])
        if(currentUser):
            userLibrary = userManager.getLibrary(currentUser[const.SQL_ID])
            libraryIDs = {game[1] for game in userLibrary}
            session['accountBalance'] = currentUser[const.SQL_BALANCE]
            return render_template("gamePage.html", game = gameInfo, relatedGames = sharedTag,
                                   userInfo = currentUser, libraryIDs = libraryIDs)
        else:
            return render_template("gamePage.html", game = gameInfo, relatedGames = sharedTag)
    else:
        return redirect('/games')


