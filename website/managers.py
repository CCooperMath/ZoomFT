from .datatypes import User, Game, Tag
from .interfacing import Interfacer
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
        #Query for username in database 
        try:
            self.interfacer.execute('SELECT 1 FROM Users WHERE Username = %s', (username, ))
            result = self.interfacer.fetchone()
            return (result != None)

        except Exception as e:
            print(e)

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
        try:
            self.interfacer.execute('SELECT 1 FROM Users WHERE Username = %s AND Pass = %s',
                                    (username,password))
            return (self.interfacer.fetchone() != None)
        except Exception as e:
            print(e)

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
        if self.checkExists(username):
            #If a given username does exist, return false to indicate that.
            return False
        else:
            #If a given username does not exist, create the user and return true. 
            newUser = User(username,password,balance,administrator)
            print(newUser.astuple())
            self.interfacer.execute('INSERT INTO Users(Username,Pass,Balance,Administrator) VALUES (%s,%s,%s,%s)',
                                    newUser.astuple())
            return True  

    def getUser(self,username):
        """ Fetches a user from the query for a given username. 

        Parameters 
        ----------
        username: string
            A string representing the user to fetch.

        Returns
        ----------
        userInfo : User
            A User object representing the user that was fetched.

        """
        self.interfacer.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        databaseID, *userInfo = self.interfacer.fetchall()[0]
        print(userInfo)
        return User(*userInfo)
    

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
            session['username'] = username
            print(self.getUser(username).administrator)
            session['administrator'] = self.getUser(username).administrator 
            print("Signed in.")
            return True
        else:
            print("Failed to sign in.")
            return False 

    def logout(self):
        """ Logs out a user by modifying the session variables 
        for username and administrator. 
        """

        session['username'] = None
        session['administrator'] = False


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

    def changeUsername(self, startName, endName):
        """ Changes the username for a user.

        Parameters 
        ----------
        startName: string
            The original username for a user. 
        endName: string
            The desired username for said user.

        Returns
        ----------
        True if the username was successfully changed. False if otherwise. 
        """

        return

    def changePassword(self, username, newPassword):
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
        return

    def getUser(self,username):
        """ Fetches a user from the query for a given username. 

        Parameters 
        ----------
        username: string
            A string representing the user to fetch.

        Returns
        ----------
        userInfo : User
            A User object representing the user that was fetched.

        """
        self.interfacer.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        databaseID, *userInfo = self.interfacer.fetchall()[0]
        print(userInfo)
        return User(*userInfo)

    def getAllUsers(self):
        # Adds a friendship between user1 and user2
        """ Fetches all Users from the Users table of the SQL database. 

        Returns
        ----------
        An iterator over all tuples representing the users in the database. 
        """
        self.interfacer.execute("SELECT * FROM Users",None)
        return self.interfacer.fetchall()

    def getLibrary(self, username):
        """ Fetches all games owned by a specific user from the SQL database. 
        
        Parameters 
        ----------
        username: string
            A string representing the username whose library we want

        Returns
        ----------
        An iterator over all tuples representing the games owned by a specific user.

        """
        return 

    def getFriendsOf(self, username):
        """ Fetches all friends of a specific user from the SQL database. 
        
        Parameters 
        ----------
        username: string
            A string representing the username whose friends we want.

        Returns
        ----------
        An iterator over all tuples representing the friends of a specific user. 

        """
        # Returns a list of names that are friends 
        return

    def addFriend(self, user1, user2):
        """ Adds a friendship between two users to the SQL database.
        Note that the friendship is added in both directions.

        Parameters 
        ----------
        user1: string
            The username of one of the users.
        user2: string
            The username of the other user.

        Returns
        ----------
        True if the friendship was successfully added. False if the friendship was not.

        """

        return 

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

    def getAllGames(self):
        """ Fetches all games from the SQL Database. 

        Returns
        ----------
        An iterator over all tuples representing the games in the SQL Database. None if the
        database is empty. 

        """
        return 

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
        return 

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
        return

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
        return

    def getGame(self, title):
        """ Fetches a game from the SQL Database. 

        Parameters 
        ----------
        title: string
            A string representing the title of the game we want to fetch.

        Returns
        ----------
        A Game object representing the game that was fetched. If the game is not found, returns None.

        """
        return 

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
        return 

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

    def getAllTags(self):
        """ Fetches all tags that currently exist in the SQL Database.

        Returns
        ----------
        An iterator over all tuples representing the tags in the SQL Database.
        None if no tags exist in the database. 

        """
        return

    def getTag(self, tag):
        """ Fetches a tag from the SQL database. 

        Parameters 
        ----------
        tag: string
            The name of the tag to fetch. 

        Returns
        ----------
        An instance of the Tag object. 

        """
        return

    def checkExists(self, tag):
        """ Queries whether a given tag already exists in the SQL database. 

        Parameters 
        ----------
        tag: string
            The name of the tag to check existence of.

        Returns
        ----------
        True if the tag exists. False if otherwise. 

        """
        return

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
        return 






