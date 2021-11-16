from flask import request
from models import *

def getRegisterData():
    name = request.form['name']
    lastName = request.form['lastName']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    return name, lastName, email, username, password

def validateLoginCredentials(db_session, username, password):
    # Check wether is an admin or client user
    adminQuery = db_session.query(Administrator)
    clientQuery = db_session.query(Client)
    adminFilter = adminQuery.filter(Administrator.username == username)
    clientFilter = adminQuery.filter(Client.username == username)
    isAdmin = None # Username not found as default
    passwordFilter = None # Predefine passwordFilter variable
    # Check type of user
    if adminFilter.count() == 1:
        isAdmin = True
    elif clientFilter.count() == 1:
        isAdmin = False
    # Check password
    if isAdmin:
        passwordFilter = adminQuery.filter(Administrator.password == password)
    else:
        passwordFilter = clientQuery.filter(Client.password == password)
    isPasswordCorrect = passwordFilter.count() == 1
    if isPasswordCorrect:
        return isAdmin
    else:
        return None