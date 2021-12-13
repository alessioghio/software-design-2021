import dash
from sqlalchemy import and_
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
#from sqlalchemy.sql.expression import and_
from dash_app_folder.dash_application import create_dash_application
import os
from models import *
from utils import *
import plotly.express as px
# from dash_application import create_dash_application # Llamar a la función que crea la página dash
from dash.dependencies import Input, Output


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    # Using a development configuration
    app.config.from_object('config.DevConfig')
else:
    # Using a production configuration
    app.config.from_object('config.ProdConfig')

db = Manager()
engine = db.createEngine(ENV)

dash_app,data_frame = create_dash_application(app,engine)

@app.route('/')
def index():
    sessionType = "None"
    if "admin" in session:
        sessionType = "adminSession"
    elif "client" in session:
        sessionType = "clientSession"
    # Get available startups
    db_session = db.getSession(engine)
    startups = db_session.query(Adminurl).all()
    return render_template('index.html', sessionType=sessionType, startups=startups)

@app.route('/login')
def login():
    if "admin" in session or "client" in session:
        return redirect(url_for('user'))
    else:
        # Get available startups
        db_session = db.getSession(engine)
        startups = db_session.query(Adminurl).all()
        return render_template('login.html', startups=startups)

@app.route('/registerAdmin')
def registerAdmin():
    return render_template('registerAdmin.html')

@app.route('/registerClient')
def registerClient():
    return render_template('registerClient.html')

@app.route('/success')
def success():
    return render_template('successDummy.html')

@app.route('/error')
def error():
    return render_template('errorDummy.html')

@app.route('/user/sales')
def sales():
    sessionType = "adminSession"
    return render_template('sales.html', sessionType=sessionType)

@app.route('/user/newProduct')
def newProduct():
    # Get all categories
    db_session = db.getSession(engine)
    supplies = getAdminSupplies(db_session, session["admin"])
    categories = getUniqueCategories(supplies)
    sessionType = "adminSession"
    return render_template('newProduct.html', sessionType=sessionType, categories=categories)

@app.route('/user/productsAdmin')
def productsAdmin():
    db_session = db.getSession(engine)
    supplies = getAdminSupplies(db_session, session["admin"])
    sessionType = "adminSession"
    return render_template('productsAdmin.html', sessionType=sessionType, supplies=supplies, os=os)

@app.route('/user/recipesAdmin')
def recipesAdmin():
    sessionType = "adminSession"
    return render_template('recipesAdmin.html', sessionType=sessionType)

@app.route('/newProductRequest', methods=['POST'])
def newProductRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, price, unit, category, description, visibility, image = getNewProductData()
        if nameExists(db_session, Supply, name):
            flash('Insumo existente.')
            return redirect(url_for('newProduct'))
        else:
            # Save into db
            data = Supply(name=name, price=price, unit=unit, visibility=visibility,
                        category=category, description=description, admin_id=session["admin"])
            db_session.add(data)
            db_session.commit()
            # Save image
            imagePath = getProductImagePath(db_session, image, name)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagePath))
            flash('Insumo creado.')
            return redirect(url_for('newProduct'))

@app.route('/user/newStock')
def newStock():
    db_session = db.getSession(engine)
    supplyQuery = db_session.query(Supply)
    supplies = supplyQuery.filter(Supply.admin_id == session["admin"]).all()
    sessionType = "adminSession"
    return render_template('newStock.html', sessionType=sessionType, supplies=supplies)

@app.route('/newStockRequest', methods=['POST'])
def newStockRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name = request.form['name']
        quantity = request.form['quantity']
        quantity = int(quantity)
        # Get previous amount
        supplyQuery = db_session.query(Supply)
        supply = supplyQuery.filter(Supply.name == name).first()
        prevQuantity = supply.quantity if supply.quantity is not None else 0
        # update
        quantity += prevQuantity
        db_session.query(Supply).\
            filter(Supply.id == supply.id).\
            filter(Supply.admin_id == session["admin"]).\
            update({"quantity": quantity})
        db_session.commit()
        flash('Stock agregado.')
        return redirect(url_for('newStock'))

@app.route('/user/newRecipe')
def newRecipe():
    sessionType = "adminSession"
    db_session = db.getSession(engine)
    supplyQuery = db_session.query(Supply)
    supplies = supplyQuery.filter(Supply.admin_id == session["admin"]).all()
    return render_template('newRecipe.html', sessionType=sessionType, supplies=supplies)

@app.route('/newRecipeRequest')
def newRecipeRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, supply_id_list, price, category, visibility, description, image = getNewRecipeData()
        if nameExists(db_session, Recipe, name):
            flash('Receta existente.')
            return redirect(url_for('newRecipe'))
        else:
            # Insert data on db
            data = Recipe(name=name, price=price, category=category, visibility=visibility, description=description, admin_id=session["admin"])
            db_session.add(data)
            db_session.commit()
            # Save image
            imagePath = getProductImagePath1(db_session, image, name)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagePath))
            flash('Receta creada.')
            return redirect(url_for('newRecipe'))

@app.route('/registerRequestAdmin', methods=['POST'])
def registerRequestAdmin():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, lastName, email, username, password, startup = getRegisterData()
        clientUserExists = userExists(db_session, Client, username, email)
        adminUserExists = userExists(db_session, Administrator, username, email)
        if clientUserExists or adminUserExists:
            flash('Usuario o correo ya existen.')
            return redirect(url_for('registerAdmin'))
        if not(adminUserExists):
            userType="Admin"
            adminClass = Administrator(name=name, lastName=lastName, email=email,
                                username=username, password=password, userType=userType)
            db_session.add(adminClass)
            db_session.commit()
            # Get new admin id
            adminQuery = db_session.query(Administrator)
            admin = adminQuery.filter(Administrator.username == username).first()
            print(f"ADMIN ID: {admin.id}")
            adminStartup = Adminurl(name=startup, admin_id=admin.id)
            db_session.add(adminStartup)
            db_session.commit()
            return redirect(url_for('login'))

@app.route('/registerRequestClient', methods=['POST'])
def registerRequestClient():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, lastName, email, username, password, _ = getRegisterData()
        clientUserExists = userExists(db_session, Client, username, email)
        adminUserExists = userExists(db_session, Administrator, username, email)
        if clientUserExists or adminUserExists:
            flash('Usuario o correo ya existen.')
            return redirect(url_for('registerAdmin'))
        if not(clientUserExists):
            userType="Client"
            data = Client(name=name, lastName=lastName, email=email,
                        username=username, password=password, userType=userType)
            db_session.add(data)
            db_session.commit()
            return redirect(url_for('login'))

@app.route('/loginRequest', methods=['POST'])
def loginRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        username = request.form['username']
        password = request.form['password']
        isAdmin = validateLoginCredentials(db_session, username, password)
        if isAdmin is not None:
            if isAdmin:
                idQuery = db_session.query(Administrator)
                admin = idQuery.filter(Administrator.username == username).first()
                session["admin"] = admin.id
            else:
                idQuery = db_session.query(Client)
                client = idQuery.filter(Client.username == username).first()
                session["client"] = client.id
            return redirect(url_for('user'))
        else:
            flash('Usuario o contraseña incorrectas.')
            return redirect(url_for('login'))

@app.route('/user/admin')
def adminProfile():
    sessionType = "adminSession"
    return render_template('profile-stocker.html', sessionType=sessionType)

@app.route('/user/client')
def clientProfile():
    sessionType = "clientSession"
    # Get available startups
    db_session = db.getSession(engine)
    startups = db_session.query(Adminurl).all()
    return render_template('profile-client.html', sessionType=sessionType, startups=startups)

@app.route('/user')
def user():
    if "admin" in session:
        return redirect(url_for('adminProfile'))
    elif "client" in session:
        return redirect(url_for('clientProfile'))
    else:
        return redirect(url_for('error'))

@app.route('/logout')
def logout():
    if "admin" in session:
        session.pop('admin', None)
    elif "client" in session:
        session.pop('client', None)
    else:
        return redirect(url_for('error'))
    flash('Sesión cerrada.')
    return redirect(url_for('login'))

@app.route('/user/updateStock')
def update():
    db_session = db.getSession(engine)
    supplies = getAdminSupplies(db_session, session["admin"])
    categories = getUniqueCategories(supplies)
    sessionType = "adminSession"
    return render_template('newUpdate.html', sessionType=sessionType, supplies=supplies, categories=categories)

@app.route('/user/updateRequest', methods=['POST'])
def updateRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        updateData = getUpdateData()
        id = updateData[0]
        updateData = updateData[1:]
        supplyQuery = db_session.query(Supply)
        supply = supplyQuery.filter(Supply.id == id).first()
        attributes = ["name", "price", "quantity", "unit", "category", "visibility", "description"]
        indices = [0, 1, 2, 3, 4, 5, 6]
        for idx, data, attribute in zip(indices, updateData, attributes):
            if data == "":
                updateData[idx] = supply.__getattribute__(attribute)
        name = updateData[0]
        price = updateData[1]
        quantity = updateData[2]
        unit = updateData[3]
        category = updateData[4]
        visibility = updateData[5]
        description = updateData[6]
        image = updateData[7]
        db_session.query(Supply).\
            filter(Supply.id == id).\
            filter(Supply.admin_id == session["admin"]).\
            update({"name": name,
                    "price": price,
                    "quantity": quantity,
                    "unit": unit,
                    "category": category,
                    "visibility": visibility,
                    "description": description})
        db_session.commit()
        # Save image
        if secure_filename(image.filename) != "":
            imagePath = getProductImagePath(db_session, image, name)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagePath))
        flash('Información actualizada.')
        return redirect(url_for('update'))

@app.route('/fillForm', methods=['POST'])
def fillForm():
    if request.method == "POST":
        request.get_data()
        id = request.data.decode('UTF-8') # Javascript return binary string
        id = int(id[1:-1])
        db_session = db.getSession(engine)
        supplyQuery = db_session.query(Supply)
        supply = supplyQuery.filter(Supply.id == id).first()
        data = {"name": supply.name,
                "price": supply.price,
                "quantity": supply.quantity,
                "category": supply.category,
                "unit": supply.unit,
                "visibility": supply.visibility,
                "description": supply.description}
        return jsonify(data)

@app.route('/fillClientData', methods=['POST'])
def fillClientData():
    if request.method == "POST":
        db_session = db.getSession(engine)
        clientQuery = db_session.query(Client)
        client = clientQuery.filter(Client.id == session['client']).first()
        data = {"name": client.name,
                "lastName": client.lastName,
                "email": client.email,
                "username": client.username}
        return jsonify(data)

@app.route('/startup/<name>')
def startup(name):
    db_session = db.getSession(engine)
    startupQuery = db_session.query(Adminurl)
    startup = startupQuery.filter(Adminurl.name == name).first()
    # Get visible stock
    supplies = getAdminSupplies(db_session, startup.admin_id)
    for supply in supplies:
        if not(supply.visibility):
            supplies.remove(supply)
    # Get available startups
    startups = db_session.query(Adminurl).all()
    if "admin" in session:
        sessionType = "adminSession"
    elif "client" in session:
        sessionType = "clientSession"
    else:
        sessionType = "None"
    return render_template('home-client.html', startups=startups, startupName=startup.name, supplies=supplies, os=os, sessionType=sessionType)

@dash_app.callback(
    Output('tabla-supply','figure'),
    Input('category-supply','value')
)
def update_graph(category_supply):
    if category_supply == 'price':
        fig = px.bar(data_frame, x="name", y="price", color="category", barmode="group",
                labels={"name":"Productos","quantity":"Cantidad","category":"Categoría"})
    elif category_supply == 'quantity':
        fig = px.bar(data_frame, x="name", y="quantity", color="category", barmode="group",
            labels={"name":"Productos","quantity":"Cantidad","category":"Categoría"})
    return fig

if __name__ == '__main__':
    app.run()