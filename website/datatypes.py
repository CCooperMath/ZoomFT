from . import constants  as const

class User:
    """
    A class representing all necessary user data.

    attributes:
    userID: int 
        A integer representing a users ID. 
    username: string
        A string representing a users username. 
    password: string 
        A string representing a users password.
    balance: decimal
        A decimal value representing the current account balance. 
    administrator:
        A boolean value representing whether the user is an administrator
        or not. 
    """
    def __init__(self,userID,username,password,balance = 0.0 ,administrator = 0):
        """ Initializes the User object. The initializer does NOT perform
        any input sanitation. The initializer DOES provide default values
        for balance and administrator. 

        Parameters
        ----------
        userID: Int
        username: String
        password: String
        balance: Decimal
        administrator: Boolean 
        
        Returns
        -------
        User object 
        """
        self.userID = userID
        self.username = username
        self.password = password
        self.balance = balance
        self.administrator = administrator
    
    def astuple(self):
        """ 
        Returns the User object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that the id
        in the SQL database is NOT included here. 
        """
        return (self.userID,self.username,self.password,self.balance,self.administrator)

class Game:
    """
    A class representing all necessary user data.

    attributes:
    gameID: int
        An integer representing the games ID. 
    title: string
        A string representing the title of the game.
    price: decimal
        A decimal representing the price of the game. 
    """
    def __init__(self, gameID, title, price):
        """ Initializes the Game object. The initializer does NOT
        perform any input sanitation. 

        Parameters
        ----------
        gameID: int 
        title: String
        price: Decimal
        
        Returns
        -------
        Game object 
        """
        self.gameID = gameID
        self.title = title
        self.price = price
    
    def astuple(self):
        """ 
        Returns the Game object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that 
        the id in the SQL database is NOT included here.
        """
        return (self.gameID, self.title,self.price)

class Review:
    """
    A class representing all necessary user data.

    attributes:
    reviewID: int
        An integer representing the reviews ID. 
    gameTitle: string
        A string representing the title of the game the 
        review is for. 
    authorName: string
        A string representing the name of the author of
        the review. 
    body: string
        A string representing the body of the review. 

    """
    def __init__(self,reviewID, gameTitle,authorName,body, rating):
        """ Initializes the Review object. The initializer
        does NOT perform any input sanitation. 

        Parameters
        ----------
        gameTitle : String
            The title of the game the review is for. NOT 
            the Game object.
        authorName: String
            The author of the game the review is for. NOT
            the User object.
        body: String
            The text representing the body of the review.
        rating: Int
            The rating (in stars from 1-5) the review provides
            for the game.
        
        Returns
        -------
        Review object 
        """
        self.reviewID = reviewID
        self.game = game
        self.author = author
        self.body = body
        self.rating = rating

    def astuple(self):
        """ 
        Returns the Review object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that 
        the id in the SQL database is not included here.
        """
        return (self.reviewID, self.game,self.author,self.body)

class Tag:
    """
    A class representing all necessary tag data.

    attributes:
    tagID: int
    name: string
        A string representing a tags name.
    """
    def __init__(self, tagID, name):
        """ Initializes the Tag object. The initializer does NOT
        perform any input sanitation. 

        Parameters
        ----------
        name: String
            The name of the tag
        
        Returns
        -------
        Tag object 
        """
        self.tagID = tagID
        self.name = name

    def astuple(self):
        """ 
        Returns the Tag object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that 
        the id in the SQL database is NOT included here.
        """
        return (self.tagID, self.name)

