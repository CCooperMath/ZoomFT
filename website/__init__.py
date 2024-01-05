#! /usr/bin/env/ python

from flask import Flask, session
from .interfacing import Interfacer
from .managers import LoginManager, UserManager, GameManager, TagManager
from .generateFakeData import generateData

config = { 
        'host' : ,
        'port' : ,
        'user' : ,
        'password' : ,
        'database' : 'ZoomFront' 
}

# Create the Flask application and set its secret key.
interfacer = Interfacer(config)
loginManager = LoginManager(interfacer)
tagManager = TagManager(interfacer)
userManager = UserManager(interfacer)
gameManager = GameManager(interfacer)

# Database initialization 



def initialize():
    generateData()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'W3lcomeToZO0MFR0NT'

    # Register views and auth blueprints.
    from .views import views 
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth")

    return app
