#! /usr/bin/env python

from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import lm
from .datatypes import User
auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        loginData = request.form
        username = request.form.get('username')
        password = request.form.get('password')

        if(lm.login(username,password)):
            return redirect(url_for('views.home'))
        else:
            print("YO!")
    
    return render_template("login.html")

@auth.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == "POST":
        lm.logout()
        return redirect(url_for('views.home'))
    return render_template("logout.html")

@auth.route('/createAccount', methods=['GET','POST'])
def createAccount():

    if request.method == "POST":
        accountData = request.form
        username = request.form.get('username')
        password = request.form.get('password')

        success = lm.createAccount(username,password)
        if(success):
            return redirect(url_for('auth.login'))
        else:
            print("FUCK!")

    return render_template("createAccount.html")

@auth.route('/settings', methods=['GET','POST'])
def settings():
    return render_template("settings.html")
