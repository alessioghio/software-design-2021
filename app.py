from math import e
import dash
from sqlalchemy import and_
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sqlalchemy.sql.expression import column
#from sqlalchemy.sql.expression import and_
from dash_app_folder.dash_application import create_dash_application
import os
import math
from datetime import datetime
from models import *
from utils import *
import plotly.express as px
# from dash_application import create_dash_application # Llamar a la función que crea la página dash
from dash.dependencies import Input, Output
import pandas as pd
from dash import html
# import plotly.graph_objects as go

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    # Using a development configuration
    app.config.from_object('config.DevConfig')
else:
    # Using a production configuration
    app.config.from_object('config.ProdConfig')

db = Manager()
engine = db.createEngine(ENV)



dash_app = create_dash_application(app,engine)

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
    # Get transactions, if any
    db_session = db.getSession(engine)
    transactionsQuery = db_session.query(Transaction)
    transactions = transactionsQuery.filter(Transaction.admin_id == session['admin']).all()
    return render_template('sales.html', sessionType=sessionType, transactions=transactions)

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
    # Get and process recipes
    db_session = db.getSession(engine)
    recipes = processRecipes(db_session, session["admin"])
    print(recipes)
    return render_template('recipesAdmin.html', sessionType=sessionType, recipes=recipes, os=os)

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
    recipeQuery = db_session.query(Recipe)
    supplies = supplyQuery.filter(Supply.admin_id == session["admin"]).all()
    rec_categories = recipeQuery.filter(Recipe.admin_id == session["admin"]).all()
    rec_categories = getUniqueCategories(rec_categories)
    print(rec_categories)
    return render_template('newRecipe.html', sessionType=sessionType, supplies=supplies, rec_categories=rec_categories)

@app.route('/newRecipeRequest', methods=['POST'])
def newRecipeRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, supply_id_list, supply_quantity_list, category, price, visibility, description, image = getNewRecipeData()
        print('Categoria:', category)
        if nameExists(db_session, Recipe, name):
            flash('Receta existente.')
            return redirect(url_for('newRecipe'))
        else:
            # Insert data on db
            supply_quantity=[]
            for i in range(len(supply_quantity_list)):
                if supply_quantity_list[i] != '0':
                    supply_quantity.append(supply_quantity_list[i])
            
            for supply_id, supply_quantity in zip(supply_id_list, supply_quantity):
                data = Recipe(name=name, price=price, category=category, supply_id=supply_id, quantity=supply_quantity, 
                                visibility=visibility, description=description, admin_id=session["admin"])
                db_session.add(data)
                db_session.commit()
            # Save image
            imagePath = getRecipeImagePath(db_session, image, name, session['admin'])
            image.save(os.path.join(app.config['UPLOAD_FOLDER2'], imagePath))
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

@app.route('/user/client', methods=["POST", "GET"])
def clientProfile():
    sessionType = "clientSession"
    # Get available startups
    db_session = db.getSession(engine)
    startups = db_session.query(Adminurl).all()
    # Get cart items, if any
    products, totalPrice = getShoppingCartItems(db_session)
    # Get transactions, if any
    transactionsQuery = db_session.query(Transaction)
    transactions = transactionsQuery.filter(Transaction.client_id == session['client']).all()
    # Get client data
    clientQuery = db_session.query(Client)
    clientData = clientQuery.filter(Client.id == session["client"]).all()
    return render_template('profile-client.html', sessionType=sessionType, startups=startups, 
                            products=products, totalPrice=totalPrice, transactions=transactions,
                            clientData=clientData)

@app.route('/user/client/updateDataRequest', methods=['POST'])
def updateClientData():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        clientQuery = db_session.query(Client)
        name = request.form["name"]
        lastname = request.form["lastName"]
        email = request.form["email"]
        username = request.form["username"]
        
        clientQuery.filter(Client.id == session["client"]).\
                                update({"name": name,
                                        "lastName": lastname,
                                        "email": email,
                                        "username": username})
        db_session.commit()
        flash('Informacion actualizada')
        return redirect(url_for('user'))

@app.route('/user/client/addCardRequest', methods=["POST", "GET"])
def addCardRequest():
    if request.method == "POST":
        number = request.form["number"]
        db_session = db.getSession(engine)
        clientQuery = db_session.query(Client)
        clientQuery.filter(Client.id == session["client"]).\
            update({"cardnumber": number})
        db_session.commit()
        flash('Tarjeta guardada.')
        return redirect(url_for('user'))

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
    allSupplies = getAdminSupplies(db_session, startup.admin_id)
    supplies = []
    for supply in allSupplies:
        if supply.visibility and supply.quantity > 0:
            supplies.append(supply)
    # Process and get recipes
    recipes = processRecipes(db_session, startup.admin_id)
    # Get available startups for display
    startups = db_session.query(Adminurl).all()
    # Get cart items if any
    products, totalPrice = getShoppingCartItems(db_session)
    # Get session type for header
    if "admin" in session:
        sessionType = "adminSession"
    elif "client" in session:
        sessionType = "clientSession"
    else:
        sessionType = "None"
    return render_template('home-client.html', startups=startups, startupName=startup.name, 
                            supplies=supplies, os=os, sessionType=sessionType, products=products,
                            totalPrice=totalPrice, recipes=recipes)

@app.route('/addToShoppingCart', methods=['POST'])
def addToShoppingCart():
    if request.method == "POST":
        db_session = db.getSession(engine)
        # Get the catalogue admin id
        startupName = request.form.get("startup")
        # Get target supply
        supply_id = request.form.get("supply_id")
        supply_id = int(supply_id)
        # Add to shopping cart
        quantity = request.form.get("quantity")
        quantity = int(quantity)
        # If supply already exists on table, update information
        cartQuery = db_session.query(ShoppingCart).\
            filter(ShoppingCart.supply_id == supply_id).\
            filter(ShoppingCart.client_id == session["client"]) 
        if cartQuery.first() is not None:
            cart = cartQuery.first()
            cartQuery.update({"quantity": cart.quantity+quantity,
                              "datetime": datetime.now()})
            db_session.commit()
            _, totalPrice = getShoppingCartItems(db_session)
            data = {"datetime": cart.datetime,
                "client_id": cart.client_id,
                "supply_id": cart.supply_id,
                "quantity": cart.quantity,
                "totalPrice": totalPrice}
        else: # create row in cart table, otherwise
            cart = ShoppingCart(datetime=datetime.now(), client_id=session["client"],
                                supply_id=supply_id, quantity=quantity)
            db_session.add(cart)
            db_session.commit()
            products, totalPrice = getShoppingCartItems(db_session)
            product = None
            for p in products:
                if p["supply_id"] == supply_id:
                    product = p
            data = {"name": product["name"],
                    "supply_id": product["supply_id"],
                    "quantity": product["quantity"],
                    "unit": product["unit"],
                    "price": product["price"],
                    "totalPrice": totalPrice,
                    "startupName": startupName}
        return jsonify(data)

@app.route('/removeFromCart', methods=['POST'])
def removeFromCart():
    if request.method == "POST":
        request.get_data()
        supply_id = request.data.decode('UTF-8') # Javascript return binary string
        db_session = db.getSession(engine)
        cartQuery = db_session.query(ShoppingCart)
        cartQuery.filter(ShoppingCart.supply_id == supply_id).delete()
        db_session.commit()
        _, totalPrice = getShoppingCartItems(db_session)
        data = {"supply_id": supply_id,
                "totalPrice": totalPrice}
        return jsonify(data)

@app.route('/buy', methods=['POST'])
def buy():
    db_session = db.getSession(engine)
    dt = datetime.now()
    if "client" in session:
        # Get admin id
        startupName = request.form['startup']
        startupQuery = cartQuery = db_session.query(Adminurl)
        startup = startupQuery.filter(Adminurl.name == startupName).first()
        admin_id = startup.id
        # Get shopping cart ids
        cartQuery = db_session.query(ShoppingCart)
        carts = cartQuery.filter(ShoppingCart.client_id == session['client']).all()
        supplyQuery = db_session.query(Supply)
        transactionPrice = 0
        for cart in carts:
            supply = supplyQuery.\
                    filter(Supply.id == cart.supply_id).first()
            transactionPrice += supply.price*cart.quantity
            newQuantity = supply.quantity - cart.quantity
            db_session.query(Supply).\
                filter(Supply.id == cart.supply_id).\
                update({"quantity": newQuantity})
            db_session.commit()
            cartQuery.filter(ShoppingCart.id == cart.id).delete()
        transaction = Transaction(datetime=dt, client_id=session['client'], price=transactionPrice, admin_id=admin_id)
        db_session.add(transaction)
        db_session.commit()
    return redirect(url_for('user'))


@dash_app.callback(
    Output('tabla-supply','figure'),
    Input('category-supply','value')
)
def update_graph(category_supply):
    data_frame = pd.read_sql_query('select * from supply', con=engine)
    if category_supply == 'price':
        fig = px.bar(data_frame, x="name", y="price", color="category", barmode="group",
                labels={"name":"Productos","price":"Precio (S/.)","category":"Categoría"})
    elif category_supply == 'quantity':
        fig = px.bar(data_frame, x="name", y="quantity", color="category", barmode="group",
            labels={"name":"Productos","quantity":"Cantidad","category":"Categoría"})
    return fig

@dash_app.callback(
    Output('pie-supply','figure'),
    Input('category-supply','value')
)
def update_pie(category_supply):
    data_frame = pd.read_sql_query('select * from supply', con=engine)
    data_frame_edit = data_frame.groupby(['category']).sum()
    categoria_frutas = data_frame_edit.index.values
    fig_pie = px.pie(data_frame_edit,names=categoria_frutas,values=category_supply) 
    return fig_pie


@dash_app.callback(
    Output('valor-medio','data'),
    Input('table-selection','value')
)
def update_tables(elements_table):
    str_df = "select * from " + elements_table
    data_frame = pd.read_sql_query(str_df,con=engine)


    print(elements_table)
    if elements_table == 'supply':
        data_frame = data_frame.loc[:,data_frame.columns!='description']
        data_frame = data_frame.loc[:,data_frame.columns!='visibility']
        data_frame = data_frame.sort_values(by=['id'])
    elif elements_table == 'client':
        data_frame = data_frame.loc[:,data_frame.columns!='password']
        data_frame = data_frame.loc[:,data_frame.columns!='username']
    elif elements_table == 'recipe': 
        # For Recipes
        df_supply = pd.read_sql_query("select * from supply",con=engine)
        df_supply = df_supply.sort_values(by=['id'])
        data_frame = data_frame.loc[:,data_frame.columns!='description']
        data_frame = data_frame.loc[:,data_frame.columns!='visibility']
        data_frame = data_frame.loc[:,data_frame.columns!='price']
        values = data_frame['supply_id'] -1
        suplies = df_supply.iloc[values]['name'].values
        data_frame['Supplies'] = suplies
        data_frame = data_frame.loc[:,data_frame.columns!='supply_id']
        data_frame = data_frame.sort_values(by=['id'])
        data_frame = data_frame.reindex(columns=['id','name','Supplies','category','quantity','admin_id'])

    df_json = data_frame.to_json(date_format='iso',orient='split')

    return df_json

@dash_app.callback(
    Output('table-div','children'),
    Input('valor-medio','data')   
)
def update_columnstable(data_frame):
    df_n = pd.read_json(data_frame,orient='split')
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col,className="th-sm") for col in df_n.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_n.iloc[i][col]) for col in df_n.columns
            ]) for i in range(len(df_n))
        ])
    ],className='table table-striped')


@dash_app.callback(
    Output('bar-recipes','figure'),
    Input('type-food','value')
)
def update_barrecipe(type_food): 
    data_frame = pd.read_sql_query("select * from recipe",con=engine)
    df_supply = pd.read_sql_query("select * from supply",con=engine)
    df_supply = df_supply.sort_values(by=['id'])
    values = data_frame['supply_id'] - 1
    suplies = df_supply.iloc[values]['name'].values
    data_frame['Supplies'] = suplies
    new_df = data_frame.loc[data_frame['category']==type_food]
    fig  = px.bar(new_df,x='quantity',y='name',color='Supplies',orientation='h',
            title='Cantidad por receta',
            labels={'name':'Receta','quantity':'Cantidad (xkg o UN)'})
    return fig

@dash_app.callback(
    Output('cost-recipes','figure'),
    Input('type-food','value')
)
def update_recipescost(type_food):
    data_frame = pd.read_sql_query("select * from recipe",con=engine)
    new_df = data_frame.loc[data_frame['category']==type_food]
    new_df = new_df.groupby(['name']).first() 
    fig = px.bar(new_df, x=new_df.index.values, y="price", barmode="group",
            labels={"name":"Productos","price":"Precio (S/.)"})
    return fig

if __name__ == '__main__':
    app.run()