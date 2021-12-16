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
    try:
        startup = request.form['startup']
    except:
        startup = None
    return name, lastName, email, username, password, startup

def getNewProductData():
    name = request.form['name']
    price = request.form['price']
    price = float(price)
    unit = request.form['unit']
    category = request.form['category']
    if category == "":
        category = request.form['categoryRadio']
    description = request.form['description']
    visibility = True if request.form.get('visibility') else False
    image = request.files['image']
    return name, price, unit, category, description, visibility, image

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
    if category == "":
        category = request.form['categoryRadio']
    visibility = True if request.form.get('visibility') else False
    description = request.form['description']
    image = request.files['image']
    return [id, name, price, quantity, unit, category, visibility, description, image]

def getNewRecipeData():
    name = request.form["recipe-name"]
    supply_id_list = request.form.getlist('supply_id')
    supply_quantity_list = request.form.getlist('cantidad')
    price = request.form["price"]
    if price != "":
        price = float(price)
    category = request.form["category"]
    visibility = True if request.form.get('visibility') else False
    description = request.form["description"]
    image = request.files["image"]
    return name, supply_id_list, supply_quantity_list, category, price, visibility, description, image

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

def getUniqueCategories(supplies):
    categories = []
    for supply in supplies:
        if supply.category not in categories:
            categories.append(supply.category)
    return categories

def getProductImagePath1(db_session, image, name):
    # Get id
    recipeQuery = db_session.query(Recipe)
    recipe = recipeQuery.filter(Recipe.name == name).first()
    filename = secure_filename(image.filename)
    # get file extension
    ext = filename.split(".")
    ext = ext[-1]
    return f"{recipe.id}.{ext}"

def getShoppingCartItems(db_session):
    cart = db_session.query(ShoppingCart).all()
    totalPrice = 0
    products = []
    for cartProduct in cart:
        dictElement = {}
        supplyProduct = db_session.query(Supply).filter(Supply.id == cartProduct.supply_id).first()
        dictElement["name"] = supplyProduct.name
        dictElement["quantity"] = cartProduct.quantity
        if supplyProduct.unit == "xkg":
            dictElement["unit"] = "kg"
        else:
            dictElement["unit"] = "UN"
        dictElement["price"] = supplyProduct.price
        dictElement["supply_id"] = supplyProduct.id
        totalPrice += dictElement["price"]*dictElement["quantity"]
        products.append(dictElement)
    return products, totalPrice
