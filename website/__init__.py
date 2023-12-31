#! /usr/bin/env/ python

from flask import Flask, session
from .interfacing import Interfacer
from .managers import LoginManager, UserManager, GameManager, TagManager



config = { 
        'host' : '127.0.0.1',
        'port' : 3306,
        'user' : 'root',
        'password' : 'Yuh',
        'database' : 'ZoomFront' 
}

# Create the Flask application and set its secret key.
db = Interfacer(config)
lm = LoginManager(db)
tm = TagManager(db)
um = UserManager(db)
gm = GameManager(db)

# Database initialization 

def initialize():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'W3lcomeToZO0MFR0NT'

    # Register views and auth blueprints.
    from .views import views 
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth")

    return app
