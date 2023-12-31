class User:
    def __init__(self,username,password,balance = 0.0 ,administrator = 0):
        self.username = username
        self.password = password
        self.balance = balance
        self.administrator = administrator
    
    def astuple(self):
        return (self.username,self.password,self.balance,self.administrator)

class Game:
    def __init__(self, title, price):
        self.title = title
        self.price = price
    
    def astuple(self):
        return (self.title,self.price)

class Review:
    def __init__(self,game,author,body):
        self.game = game
        self.author = author
        self.body = body

    def astuple(self):
        return (self.game,self.author,self.body)

class Tag:
    def __init__(self, name):
        self.name = name

    def astuple(self):
        return (self.name)

