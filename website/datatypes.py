class User:
    """
    A class representing all necessary user data.

    attributes:
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
    def __init__(self,username,password,balance = 0.0 ,administrator = 0):
        """ Initializes the User object. The initializer does NOT perform
        any input sanitation. The initializer DOES provide default values
        for balance and administrator. 

        Parameters
        ----------
        username: String
        password: String
        balance: Decimal
        administrator: Boolean 
        
        Returns
        -------
        User object 
        """
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
        return (self.username,self.password,self.balance,self.administrator)

class Game:
    """
    A class representing all necessary user data.

    attributes:
    title: string
        A string representing the title of the game.
    price: decimal
        A decimal representing the price of the game. 
    """
    def __init__(self, title, price):
        """ Initializes the Game object. The initializer does NOT
        perform any input sanitation. 

        Parameters
        ----------
        title: String
        price: Decimal
        
        Returns
        -------
        Game object 
        """
        self.title = title
        self.price = price
    
    def astuple(self):
        """ 
        Returns the Game object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that 
        the id in the SQL database is NOT included here.
        """
        return (self.title,self.price)

class Review:
    """
    A class representing all necessary user data.

    attributes:
    gameTitle: string
        A string representing the title of the game the 
        review is for. 
    authorName: string
        A string representing the name of the author of
        the review. 
    body: string
        A string representing the body of the review. 

    """
    def __init__(self,gameTitle,authorName,body, rating):
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
        return (self.game,self.author,self.body)

class Tag:
    """
    A class representing all necessary tag data.

    attributes:
    name: string
        A string representing a tags name.
    """
    def __init__(self, name):
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
        self.name = name

    def astuple(self):
        """ 
        Returns the Tag object in the form of a tuple for 
        ease of compatibility with SQL queries. Note that 
        the id in the SQL database is NOT included here.
        """
        return (self.name)

