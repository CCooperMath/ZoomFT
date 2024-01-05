from .datatypes import User, Game, Tag
from .interfacing import Interfacer
from . import constants as const
from flask import session

class LoginManager:
    """ A manager designed for handling 
    queries for logging in, signing out, 
    and creating accounts.

    Attributes: 
        interfacer: A Interfacer object which handles the SQL connection.

    """
    def __init__(self,interfacer):
        """ Initializes the LoginManager object
        Parameters 
        ----------
        interfacer: Interfacer object
            An existing Interfacer which will handle all SQL queries 
            and connection.

        Returns
        ----------
        A LoginManager object.
        """
        self.interfacer = interfacer

    def checkExists(self, username):
        """ Checks if a given username exists within the database
        Parameters 
        ----------
        username: string
            The username to query for.
        
        Returns
        ----------
        True if the username is in the database. False if otherwise. 

        """
        result = self.interfacer.getFromReference('Users','Username',username)
        return (result != []) 

    def checkPassword(self, username, password):
        """ Checks if a given password matches with a given username in the database 

        Parameters 
        ----------
        username: string
            The username whose password we are checking.
        password: string
            The proposed password.

        Returns
        ----------
        True if the username and password are correct. False if otherwise.
        """
        userInfo = self.interfacer.getFromReference('Users','Username',username)
        if userInfo:
            if(userInfo[0][const.SQL_PASSWORD] == password):
                return True
        return False 

    def createAccount(self, username, password, balance = 0.0, administrator = 0.0):
        """ Creates a user account and handles the checks for existence of the user already.

        Parameters 
        ----------
        username: string
            The username for the new account.
        password: string
            The password for the new account.
        balance: decimal
            The initial account balance for the new account.
        administrator: int(0,1)
            A boolean integer representing whether the account
            is an administrator.

        Returns
        ---------- 
        True if the account was successfully created. False if otherwise. 

        """
        if(not self.checkExists(username)):
            print("User does not exist.")
            self.interfacer.execute('INSERT INTO Users VALUES (DEFAULT, %s, %s, %s, %s)', (username, password, balance, administrator))
            print("User created.")
            self.interfacer.commit()
            return True
        print("User already exists.")
        return False

            

    def getUser(self,username):
        """ Fetches a user from the query for a given username. 

        Parameters 
        ----------
        username: string
            A string representing the user to fetch.

        Returns
        ----------
        A tuple representing the fetched user. None if the user does not exist
        or the query fails.
        """
        try:
            user = self.interfacer.getFromReference('Users','Username',username)
            return user
        except Exception as e:
            print(e)
            return None
    

    def login(self, username, password):
        """ Attempts to log in a user with a given username and password.
        Modifies the session values for username and administrator upon
        a succcessful check for the username and password. 
        
        Parameters 
        ----------
        username: string
            A string representing the submitted username.
        password: string
            A string representing the submitted password.


        Returns
        ----------
        True if the user was successfully signed in. False if otherwise. 

        """
        if( self.checkPassword(username,password) ):
            user = self.interfacer.getFromReference('Users','Username',username)

            session['username'] = username
            session['administrator'] = user[0][const.SQL_ADMINISTRATOR]
            session['userID'] = user[0][const.SQL_ID]
            session['accountBalance'] = user[0][const.SQL_BALANCE]
            return True
        else:
            return False 

    def logout(self):
        """ Logs out a user by modifying the session variables 
        for username and administrator. 
        """

        session['username'] = None
        session['administrator'] = False
        session['userID'] = None
        session['accountbalance'] = None


class UserManager:
    """ A manager designed for handling 
    queries for user related information.

    Attributes: 
        interfacer: A Interfacer object which handles the SQL connection.

    """
    def __init__(self,interfacer):
        """ Initializes the UserManager object.
        Parameters 
        ----------
        interfacer: Interfacer object
            An existing Interfacer which will handle all SQL queries 
            and connection.

        Returns
        ----------
        A UserManager object.
        """
        self.interfacer = interfacer 

    def changeUsername(self, userID, endName):
        """ Changes the username for a user.

        Parameters 
        ----------
        userID: int
            The id for the user whose name is being changed.
        endName: string
            The desired username for said user.

        Returns
        ----------
        True if the username was successfully changed. False if otherwise. 
        """
        if not self.getUser(endName):
            success = self.interfacer.editEntry('Users','id','Username',userID,endName)
            self.interfacer.commit()
            return success
        else: 
            return False

    def changePassword(self, userID, newPassword):
        """ Changes the password for a user.

        Parameters 
        ----------
        username: string
            The username of a user. 
        newPassword: string
            The desired password for a user. 

        Returns
        ----------
        True if the password was successfully changed. False if otherwise. 
        """
        success = self.interfacer.editEntry('Users','id','Pass',userID, newPassword)
        self.interfacer.commit() 
        return success 

    def getUser(self,username):
        """ Fetches a user from the query for a given username. 

        Parameters 
        ----------
        username: string
            A string representing the user to fetch.

        Returns
        ----------
        A tuple representing the fetched user. None if the user does not exist
        or the query fails.
        """
        try:
            user = self.interfacer.getFromReference('Users','Username',username)
            return user
        except Exception as e:
            print(e)
            return None

    def getAllUsers(self):
        """ Fetches all Users from the Users table of the SQL database. 

        Returns
        ----------
        An iterator over all tuples representing the users in the database. 
        """
        self.interfacer.execute("SELECT * FROM Users", None)
        return self.interfacer.fetchall() 
    

    def addFriend(self, userID1, userID2):
        """ Adds a friendship between two users to the SQL database.
        Note that the friendship is added in both directions.

        Parameters 
        ----------
        userID1: string
            The userID of the first friend in the pair.
        userID2: string
            The userID of the second friend in the pair.

        Returns
        ----------
        True if the friendship was successfully added. False if the friendship was not.

        """
        
        success = self.interfacer.addRelation('Friends','UserID', 'FriendID', userID1, userID2)
        success = success and self.interfacer.addRelation('Friends', 'FriendID', 'UserID', userID1, userID2)
        self.interfacer.commit()
        return success

    def addFriendFromNames(self, username,friendName):
        """
        Parameters
        ----------
        username:str
            The name of one of the users in the friendship.
        friendName:str
            The name of the other user in the friendship.

        Returns
        -------
        True upon a successful addition. False if otherwise. 
        """
        userID = self.interfacer.getID('Users','Username', username)
        friendID = self.interfacer.getID('Users','Username',friendName)
        success = self.addFriend(userID,friendID)
        return success 

    def addToLibraryFromNames(self, username,gameName):
        """
        Parameters
        ----------
        username:str
            The name of a user whose library is being modified.
        gameName:str
            The name of the game in the library.

        Returns
        -------
        True upon a successful addition. False if otherwise. 
        """
        userID = self.interfacer.getID('Users','Username',username)
        gameID = self.interfacer.getID('Games','Title',gameName)
        success = self.addToLibrary(userID,gameID)
        return success

    def getFriendsOf(self, userID):
        """ Fetches all friends of a specific user from the SQL database. 
        
        Parameters 
        ----------
        username: string
            A string representing the username whose friends we want.

        Returns
        ----------
        An iterator over all tuples representing the friends of a specific user. 

        """
        # Returns a list of names that are friends with the user. 
       
        friends = self.interfacer.getRelated('Friends','Users','UserID','FriendID',userID)
        return friends

    def getFriendIDs(self, friendList):
        friendIDs= [ user[2] for user in friendList ]
        return friendIDs



    def getLibrary(self, userID):
        """ Fetches all games owned by a specific user from the SQL database. 
        
        Parameters 
        ----------
        username: string
            A string representing the username whose library we want

        Returns
        ----------
        An iterator over all tuples representing the games owned by a specific user.

        """
        gameLibrary = self.interfacer.getRelated('UserLibraries','Games','UserID','GameID',userID)
        return gameLibrary

    def addToLibrary(self, userID, gameID):
        """ Adds a game with a given title to a users library) 
        
        Parameters 
        ----------
        

        Returns 
        -------
        True if the game was successfully added to the library. False if otherwise. 
        """
        if (userID != None and gameID != None):
            success = self.interfacer.addRelation('UserLibraries','UserID','GameID',userID,gameID)
            self.interfacer.commit()
            return success
        else:
            return False
    
    def deleteFriend(self, userID, friendID):
        """ Deletes a specific friendship between userID and friendID 
        Parameters
        ----------
        userID: int
            id of the first user in the friendship.
        friendID: int
            id of the second user in the friendship.

        Returns 
        ----------
        True upon a successful deletion. False if otherwise. 
        """
        try:
            success = self.interfacer.removeRelation('Friends', 'UserID', 'FriendID', userID, friendID)
            success = success and self.interfacer.removeRelation('Friends','FriendID','UserID',userID,friendID)
            return success
        except Exception as e:
            print(e)
            return False 

    def deleteFriendships(self, userID):
        """ Deletes all entries from the SQL database for a users friendships 
        """
        success = self.interfacer.removeRelated('Friends','UserID',userID)
        success = success and self.interfacer.removeRelated('Friends', 'FriendID', userID)
        self.interfacer.commit()
        return success
        

    def deleteLibrary(self, userID):
        """ Deletes all entries from the library matching a user to a game.

        Parameters
        ----------
        username: string
            A string repesenting the username of the user whose library will be deleted.

        Returns 
        -------
        True if the library was successfully deleted. False if otherwise.
        """

        success = self.interfacer.removeRelated('UserLibraries', 'UserID', userID)
        self.interfacer.commit()
        return success

    def deleteReviews(self, userID):
        """
        Parameters 
        ----------
        username: string
            A string representing the username of the user whose reviews will be deleted. 

        Returns
        ----------
        True if the reviews were succesfully deleted. False if otherwise. 

        """
        
        success = self.interfacer.removeRelated('Reviews','AuthorID',userID)
        self.interfacer.commit()
        return success


    def deleteUser(self, userID):
        """ Deletes a user from the Users table of the SQL database. 
        This also deletes their library and active friendships. 

        Parameters
        ----------
        userID: int
            The userID of the user to delete from the database.

        returns 
        ---------
        True if the user was successfully deleted. False if otherwise. 
        """
        deletion_success = True 
        # Begin by deleting the user friendships.
        deletion_success = (deletion_success and self.deleteFriendships(userID))
        
        # Delete the users reviews. 
        deletion_success = (deletion_success and self.deleteReviews(userID))

        # Delete the users library. 
        deletion_success = (deletion_success and self.deleteLibrary(userID))

        # If all previous attempts succeeded, delete the user account. 
        try:
            self.interfacer.execute('DELETE FROM Users WHERE id = %s', (userID, ))
            self.interfacer.commit()
            self.logout()
            return True
        except Exception as e:
            print(e)
            return False 

    def changeFunds(self, userID, amt):
        """ Adds funds to a user account. If the 
        user's account balance would be negative, it does
        not execute. 

        Parameters
        ----------
        userID: int
            The user's userID in the SQL database.
        amt: float
            The amount to change the account balance by. 
            Can be positive or negative. 

        Returns
        -------
        True if the change succeeded. False if the change failed either
        due to failure of the SQL query OR due to the user now having
        negative account balance 
        """
        try:
            userBalance = self.interfacer.getFromReference('Users','id',userID)[3]
            if(userBalance + amt < 0):
                print("User would have negative balance.")
                return False 
            else:
                newBalance = userBalance + amt
                self.interfacer.editEntry('Users','id','Balance',userID,newBalance)
                return True
        except Exception as e:
            print(e)
            return False



    def logout(self):
        """ Logs out a user by modifying the session variables 
        for username and administrator. 
        """

        session['username'] = None
        session['administrator'] = False
        session['userID'] = None


class GameManager:
    """ A manager designed for handling 
    queries for game related information.

    Attributes: 
        interfacer: A Interfacer object which handles the SQL connection.

    """
    def __init__(self,interfacer):
        """ Initializes the GameManager object.
        Parameters 
        ----------
        interfacer: Interfacer object
            An existing Interfacer which will handle all SQL queries 
            and connection.

        Returns
        ----------
        A GameManager object.
        """
        self.interfacer = interfacer

    def createGame(self, title, price):
        """ Inserts a new game to the SQL Database 

        Parameters
        ----------
        title: string
            The title of the new game to be added.
        price: decimal
            The price of the game to be added.
        
        Returns 
        ----------
        True if the game was successfully added. False if otherwise. 

        """
        try:
            self.interfacer.execute('INSERT INTO Games VALUES (DEFAULT, %s, %s)', (title, price))
            self.interfacer.commit()
            return True
        except Exception as e:
            print(e)
            return False 

    def getAllGames(self):
        """ Fetches all games from the SQL Database. 

        Returns
        ----------
        An iterator over all tuples representing the games in the SQL Database. None if the
        database is empty or another failure occurs. 

        """
        try:
            self.interfacer.execute('SELECT * FROM Games',None)
            return self.interfacer.fetchall()
        except Exception as e:
            print(e)
            return None

    def getGamesWithSharedTag(self,title):
        """ Fetches all games that share a tag with a given game represented by its title. 

        Parameters 
        ----------
        title: string
            A string representing the title of the original game.

        Returns
        ----------
        An iterator over all tuples representing the games that share a tag with the original
        game in the SQL Database. None if no such games exist.
        """
        try:
            gameID = self.interfacer.getID('Games','Title',title)
            gameTags = self.interfacer.getRelated('TagRelations', 'Tags', 'GameID', 'TagID', gameID)
            
            # Use a set here to ignore duplicate games. Obviously will share a tag with itself. 
            gamesWithSharedTag = set()
            if gameTags != None:
                # The game has tags. 
                for tags in gameTags:
                    # Fetch all games with this tag.
                    games = self.interfacer.getRelated('TagRelations', 'Games', 'TagID', 'GameID', tags[1])
                    # the games variable is 100% not None, because it at least has 
                    # our input game in its list. 
                    for game in games:
                        gamesWithSharedTag.add(game)
                # The funniest thing about this function is it returns duplicate 
                # entries because two games may share different tags! This is a bug 
                # that can be fixed with some sanitation. But I am avoiding it for now.
                
                return gamesWithSharedTag 
            else: 
                return None

        except Exception as e:
            print(e)
            return None


    def getOwnersOf(self,title):
        """ Fetches all users that own a given game represented by its title.

        Parameters 
        ----------
        title: string
            A string representing the title of the game.

        Returns
        ----------
        An iterator over all tuples representing the games that share a tag with the original
        game in the SQL Database. None if no such owners exist.

        """
        try:
            gameID = self.interfacer.getID('Games','Title',title)
            owners = self.interfacer.getRelated('UserLibraries', 'Users', 'GameID', 'UserID', gameID)
            return owners
        except Exception as e:
            print(e)
            return None

    def addTag(self, title, tag):
        """ Adds a tag to a game. 

        Parameters 
        ----------
        title: string
            A string representing the title of a game to add the tag to.
        tag: string
            A string representing the tag to be added to the game.

        Returns
        ----------
        True if the tag was successfully added. False otherwise. 

        """
        try: 
            gameID = self.interfacer.getID('Games','Title', title)
            tagID = self.interfacer.getID('Tags','TagName', tag)
            self.interfacer.addRelation('TagRelations','TagID','GameID', tagID, gameID)
            self.interfacer.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getGame(self, title):
        """ Fetches a game from the SQL Database. 

        Parameters 
        ----------
        title: string
            A string representing the title of the game we want to fetch.

        Returns
        ----------
        A tuple representing the game that was fetched. If the game is not found, returns None.

        """
        result = self.interfacer.getFromReference('Games','Title',title)
        if(result!= None):
            return result[0][const.SQL_TITLE]
        else:
            return None

    def getPrice(self, title):
        """ Fetches the price of a game from the SQL Database. 

        Parameters 
        ----------
        title: string
            A string representing the title of the game we want to fetch from.

        Returns
        ----------
        The price of the game. If the game is not found, returns None. 
        """
        result = self.interfacer.getFromReference('Games','Title',title)
        if(result != None):
            return result[0][const.SQL_PRICE]
        else: 
            return None

    def deleteGame(self, title):
        """ Removes a game from the SQL Database as well as removes the relationships 
        the game has. 
        
        Parameters 
        ----------
        title: string
            The name of the game to be removed.

        Returns 
        -------
        True upon a successful deletion. False if otherwise. 

        """

        self.interfacer.commit()

class TagManager:
    """ A manager designed for handling 
    queries for tag related information.

    Attributes: 
        interfacer: A Interfacer object which handles the SQL connection.

    """
    def __init__(self, interfacer):
        """ Initializes the TagManager object.
        Parameters 
        ----------
        interfacer: Interfacer object
            An existing Interfacer which will handle all SQL queries 
            and connection.

        Returns
        ----------
        A TagManager object.
        """
        self.interfacer = interfacer

    def createTag(self, tagName):
        """ Inserts a new tag into the SQL database. 
        
        Parameters
        ----------
        tagName: string
            The name of the tag to add to the database. 

        Returns 
        -------
        True if the tag was successfully added to the SQL database. False if otherwise. 

        """

        try: 
            self.interfacer.execute('INSERT INTO Tags VALUES (DEFAULT, %s)', (tagName, ))
            self.interfacer.commit()
            return True
        except Exception as e:
            print(e)
            return False 

    def getAllTags(self):
        """ Fetches all tags that currently exist in the SQL Database.

        Returns
        ----------
        An iterator over all tuples representing the tags in the SQL Database.
        None if no tags exist in the database or if the execution fails. 

        """
        try:
            self.interfacer.execute('SELECT * FROM Tags', None)
            return self.interfacer.fetchall()
        except Exception as e:
            print(e)
            return None

    def getTag(self, tag):
        """ Fetches a tag from the SQL database.

        Parameters 
        ----------
        tag: string
            The name of the tag to fetch. 

        Returns
        ----------
        A tuple representing the tag fetched from the SQL database. None if 
        the request failed or if the tag doesnt exist. 

        """
        try:
            self.interfacer.getFromReference('Tags','TagName', tag)
            return self.interfacer.fetchall()
        except Exception as e:
            print(e)
            return None

    def checkExists(self, tagName):
        """ Queries whether a given tag already exists in the SQL database. 

        Parameters 
        ----------
        tag: string
            The name of the tag to check existence of.

        Returns
        ----------
        True if the tag exists. False if otherwise or if the request fails. 

        """
        try:
            self.interfacer.execute('SELECT 1 FROM Tags WHERE TagName = %s', (tagName, ))
            return (self.interfacer.fetchall() != None)
        except Exception as e:
            print(e)
            return False



    def getGamesWithTag(self, tag):
        """ fetches all games that have a given tag in the SQL database. 

        Parameters 
        ----------
        tag: string
            The name of the tag we are querying with.

        Returns
        ----------
        An iterator over all tuples representing the games fetched from the SQL Database.

        """
        # Fetch the id of the tag in question.
        try:
            tagID = self.interfacer.getID('Tags','TagName',tag)
            results = self.interfacer.getRelated('TagRelations','Games','TagID','GameID',tagID)
            return results
        except Exception as e:
            print(e)
            return None 

    def deleteTag(self, tag):
        """ Removes a tag from the SQL database along with all relationships it has.

        Parameters
        ----------
        tag: string
            The name of the tag we are removing.

        Returns
        -------
        True if the tag was successfully deleted from the database. False if otherwise. 
        """
        self.interfacer.commit()




