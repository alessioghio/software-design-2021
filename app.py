from flask import Flask, render_template, request, redirect, url_for, session
from models import *
from utils import *

from dash_application import create_dash_application # Llamar a la función que crea la página dash

app = Flask(__name__)
create_dash_application(app)


ENV = 'dev'

if ENV == 'dev':
    # Using a development configuration
    app.config.from_object('config.DevConfig')
else:
    # Using a production configuration
    app.config.from_object('config.ProdConfig')

#db = Manager()
#engine = db.createEngine(ENV)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
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

@app.route('/home-pizza')
def home():
    return render_template('home-pizza.html')  

@app.route('/profile-stocker')
def profileAdmin():
    return render_template('profile-stocker.html')  

@app.route('/error')
def error():
    return render_template('errorDummy.html')

@app.route('/registerRequestAdmin', methods=['POST'])
def registerRequestAdmin():
    if request.method == 'POST':
        db_session = db.getSession(engine)
        name, lastName, email, username, password = getRegisterData()
        usernameExists = db_session.query(Administrator).filter(Administrator.username == username).count() > 0
        if not(usernameExists):
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
        usernameExists = db_session.query(Client).filter(Client.username == username).count() > 0
        if not(usernameExists):
            userType="Client"
            data = Client(name=name, lastName=lastName, email=email, 
                        username=username, password=password, userType=userType)        
            db_session.add(data)
            db_session.commit()
            return redirect(url_for('login'))
        return redirect(url_for('error'))

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
            return redirect(url_for('error')) 

@app.route('/user')
def user():
    username = ""
    if "admin" in session:
        username = session["admin"]
        return f"<h1> admin {username} </h1>"
    elif "client" in session:
        username = session["client"]
        return f"<h1> client {username} </h1>"
    else:
        return redirect(url_for('error'))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('loginDummy.html')

if __name__ == '__main__':
    app.run()