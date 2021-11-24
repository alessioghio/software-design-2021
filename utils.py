from flask import request
from models import *

def getRegisterData():
    name = request.form['name']
    lastName = request.form['lastName']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    return name, lastName, email, username, password

def getNewProductData():
    name = request.form['name']
    price = request.form['price']
    price = float(price)
    unit = request.form['unit']
    category = request.form['category']
    description = request.form['description']
    image = request.files['image']
    return name, price, unit, category, description, image

def getUpdateData():
    id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    price = float(price)
    quantity = request.form['quantity']
    quantity = int(quantity)
    unit = request.form['unit']
    category = request.form['category']
    visibility = request.form['visibility']
    visibility = True if visibility == "True" else False
    description = request.form['description']
    return id, name, price, quantity, unit, category, visibility, description

def validateLoginCredentials(db_session, username, password):
    # Check wether is an admin or client user
    adminQuery = db_session.query(Administrator)
    clientQuery = db_session.query(Client)
    adminFilter = adminQuery.filter(Administrator.username == username)
    clientFilter = clientQuery.filter(Client.username == username)
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
    
def userExists(db_session, table, username, email):
    usernameExists = db_session.query(table).filter(table.username == username).count() > 0
    emailExists = db_session.query(table).filter(table.email == email).count() > 0
    return usernameExists or emailExists

def nameExists(db_session, table, name):
    return db_session.query(table).filter(table.name == name).count() > 0