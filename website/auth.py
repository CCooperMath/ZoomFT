#! /usr/bin/env python

from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import session
from . import loginManager, userManager
from .datatypes import User
auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        loginData = request.form
        username = request.form.get('username')
        password = request.form.get('password')

        if(loginManager.login(username,password)):
            return redirect(url_for('views.home'))

    
    return render_template("login.html")

@auth.route('/logout', methods=['GET','POST'])
def logout():
    if request.method == "POST":
        loginManager.logout()
        return redirect(url_for('views.home'))
    return render_template("logout.html")

@auth.route('/createAccount', methods=['GET','POST'])
def createAccount():

    if request.method == "POST":
        accountData = request.form
        username = request.form.get('username')
        password = request.form.get('password')

        success = loginManager.createAccount(username,password)
        if(success):
            return redirect(url_for('auth.login'))

    return render_template("createAccount.html")

@auth.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        # Get ID of viewing user when the page 
        # was opened. Only execute this if 
        # the current session ID matches that user ID. 
        viewerID = int(request.form.get('userAtView'))
        ids = (session['userID'],viewerID)
        if(session['userID'] == viewerID):
            match request.form.get('type'):
                case 'passChange':
                    newPass = request.form.get('newPass')
                    success = userManager.changePassword(viewerID,newPass) 
                    if(not success):
                        print("Failed to change password.")
                    
                case 'nameChange':
                    newName = request.form.get('newName')
                    success = userManager.changeUsername(viewerID,newName)
                    if(not success):
                        print("Username already in use.")
                case 'deleteAccount':
                    success = userManager.deleteUser(viewerID)
                    if(not success):
                        print("Failed to delete user.")
                    else:
                        return redirect(url_for('auth.login'))
        else:
            print("viewerID to sessionID mismatch.") 
    return render_template("settings.html")
