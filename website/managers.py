from .datatypes import User, Game, Tag
from .interfacing import Interfacer
from flask import session

class LoginManager:
    def __init__(self,interfacer):
        self.interfacer = interfacer

    def checkExists(self, username):
        #Query for username in database 
        try:
            self.interfacer.execute('SELECT 1 FROM Users WHERE Username = %s', (username, ))
            result = self.interfacer.fetchone()[0]
            return (result == 1)

        except Exception as e:
            print(e)

    def checkPassword(self, username, password):
        #Query for username with matching password in database 
        try:
            self.interfacer.execute('SELECT 1 FROM Users WHERE Username = %s AND Pass = %s',
                                    (username,password))
            return (self.interfacer.fetchone() != None)
        except Exception as e:
            print(e)

    def createAccount(self, username, password, balance = 0.0, administrator = 0.0):
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
        self.interfacer.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        databaseID, *userInfo = self.interfacer.fetchall()[0]
        print(userInfo)
        return User(*userInfo)
    

    def login(self, username, password):
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
        session['username'] = None
        session['administrator'] = False


class UserManager:
    def __init__(self,interfacer):
        self.interfacer = interfacer 

    def changeUsername(self, startName, endName):
        return

    def changePassword(self, username, newPassword):
        return

    def getAllUsers(self):
        self.interfacer.execute("SELECT * FROM Users",None)
        return self.interfacer.fetchall()

    def getLibrary(self, username):
        return 

    def getFriendsOf(self, username):
        # Returns a list of names that are friends 
        return

    def addFriend(self, user1, user2):
        # Adds a friendship between user1 and user2

        return 

class GameManager:
    def __init__(self,interfacer):
        self.interfacer = interfacer

    def getAllGames(self):
        return 

    def getGamesWithSharedTag(self,title):
        return 

    def getOwnersOf(self,title):
        return

    def addTag(self, title, tag):
        return

    def getGame(self, title):
        return 

    def getPrice(title):
        return 

class TagManager:
    def __init__(self, interfacer):
        self.interfacer = interfacer

    def getAllTags(self):
        return

    def getTag(self):
        return

    def checkExists(self, tag):
        return

    def getGamesWithTag(self):
        return 






