from flask import request
from models import *
from werkzeug.utils import secure_filename
import os

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
    if price != "":
        price = float(price)
    quantity = request.form['quantity']
    if quantity != "":
        quantity = int(quantity)
    unit = request.form['unit']
    category = request.form['category']
    visibility = True if request.form.get('visibility') else False
    description = request.form['description']
    image = request.files['image']
    return [id, name, price, quantity, unit, category, visibility, description, image]

def getRecipeData():
    id_supply = request.form["supply_id"]
    return id_supply

def validateLoginCredentials(db_session, username, password):
    # Check wether is an admin or client user
    adminQuery = db_session.query(Administrator)
    clientQuery = db_session.query(Client)
    adminFilter = adminQuery.filter(Administrator.username == username)
    clientFilter = clientQuery.filter(Client.username == username)
    isAdmin = None # Username not found as default
    # Check type of user
    if adminFilter.count() == 1:
        isAdmin = True
    elif clientFilter.count() == 1:
        isAdmin = False
    # Check password
    if isAdmin:
        user = adminQuery.filter(Administrator.username == username).first()
    else:
        user = clientQuery.filter(Client.username == username).first()
    isPasswordCorrect = user.password == password and user.username == username
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

def getAdminSupplies(db_session, adminId):
    supplyQuery = db_session.query(Supply)
    supplies = supplyQuery.filter(Supply.admin_id == adminId).all()
    return supplies

def getProductImagePath(db_session, image, name):
    # Get id
    supplyQuery = db_session.query(Supply)
    supply = supplyQuery.filter(Supply.name == name).first()
    filename = secure_filename(image.filename)
    # get file extension
    ext = filename.split(".")
    ext = ext[-1]
    return f"{supply.id}.{ext}"
    