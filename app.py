from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
from utils import *

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


@app.route('/')
def index():
    sessionExists = False
    if "admin" in session or "client" in session:
        sessionExists = True
    return render_template('index.html', sessionExists=sessionExists) 

@app.route('/')
def sessions():    
    sessionAdmin = False
    sessionClient = False
    if "admin" in session:
        sessionAdmin = True   
        if "client" in session:
            sessionClient = True
        return render_template('index.html', sessionClient=sessionClient)  
    return render_template('index.html', sessionAdmin=sessionAdmin)      


@app.route('/login')
def login():
    if "admin" in session or "client" in session:
        return redirect(url_for('user'))
    else:
        return render_template('login.html')

@app.route('/registerAdmin')
def registerAdmin():
    return render_template('registerAdmin.html')

@app.route('/registerClient')
def registerClient():
    return render_template('registerClient.html')

@app.route('/success')
def success():
    return render_template('successDummy.html')

# ----- DEBUG ------ #

@app.route('/home-pizza')
def home():
    return render_template('home-pizza.html')  



# ------------------ #

@app.route('/error')
def error():
    return render_template('errorDummy.html')

@app.route('/user/newProduct')
def newProd():
    return render_template('newProduct.html')    

@app.route('/user/newStock')
def newStock():
    return render_template('newStock.html')  

@app.route('/registerRequestAdmin', methods=['POST'])
def registerRequestAdmin():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, lastName, email, username, password = getRegisterData()
        clientUserExists = userExists(db_session, Client, username, email)
        adminUserExists = userExists(db_session, Administrator, username, email)
        if clientUserExists or adminUserExists:
            flash('Usuario o correo ya existen.')
            return redirect(url_for('registerAdmin'))
        if not(adminUserExists):
            userType="Admin"
            data = Administrator(name=name, lastName=lastName, email=email, 
                                username=username, password=password, userType=userType)
            db_session.add(data)
            db_session.commit()
            return redirect(url_for('login'))

@app.route('/registerRequestClient', methods=['POST'])
def registerRequestClient():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, lastName, email, username, password = getRegisterData()
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
                session["admin"] = username
            else:
                session["client"] = username
            return redirect(url_for('user'))
        else:
            flash('Usuario o contraseña incorrectas.')
            return redirect(url_for('login'))

@app.route('/user/admin')
def adminProfile():
    return render_template('profile-stocker.html')

@app.route('/user/client')
def clientProfile():
    return render_template('profile-pizza.html')

@app.route('/user')
def user():
    if "admin" in session:
        # username = session["admin"]
        return redirect(url_for('adminProfile'))
    elif "client" in session:
        # username = session["client"]
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
    supplyQuery = db_session.query(Supply)
    data = supplyQuery.all()
    return render_template('update.html', data=data)

@app.route('/user/updateRequest', methods=['POST'])
def updateRequest():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        id, name, price, quantity, unit, category, visibility = getUpdateData()
        print(type(price))
        db_session.query(Supply).\
            filter(Supply.id == id).\
            update({"name": name,
                    "price": price,
                    "quantity": quantity,
                    "unit": unit,
                    "category": category,
                    "visibility": visibility})
        db_session.commit()
        flash('Información actualizada.')
        return redirect(url_for('update'))


if __name__ == '__main__':
    app.run()