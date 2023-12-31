#! /usr/bin/env python


from flask import Blueprint, render_template
from . import db, lm, um, tm, gm

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/users')
def user():
    userList = um.getAllUsers()
    print(userList)
    return render_template("users.html", users = userList)

@views.route('/store')
def store():
    gameList = gm.getAllUsers()
    return render_template("store.html", games = gameList)


