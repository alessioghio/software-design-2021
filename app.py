from flask import Flask, render_template, request, redirect, url_for
from models import *

# Developermust create a file named dbCredentials.py and insert the local name 
# of database and password. This file is included in the .gitignore so people's
# credentials are not mixed
from dbCredentials import database, password

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password}@localhost/{database}"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://rxaguhpxsprsvl:4cb9cf7c51e01ba4615f4b1ba2efc27e593cbd07fe751b0109b63d73d6ee5433@ec2-18-214-214-252.compute-1.amazonaws.com:5432/dc5lmvlefddiu5"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
@app.route('/login')
def index():
    return render_template('loginDummy.html')    

@app.route('/success')
def success():
    return render_template('successDummy.html')

@app.route('/error')
def error():
    return render_template('errorDummy.html')

@app.route('/registerRequest', methods=['POST'])
def registerRequest():
    if request.method == 'POST':
        name = request.form['name']
        lastName = request.form['lastName']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        usernameExists = db.session.query(Administrator).filter(Administrator.username == username).count() > 0
        if not(usernameExists):
            data = Administrator(name, lastName, email, username, password)
            db.session.add(data)
            db.session.commit()
        return redirect(url_for('login'))

@app.route('/loginRequest', methods=['GET'])
def loginRequest():
    if request.method == 'GET':
        username = request.form['username']
        password = request.form['password']
        # Check wether is an admin or client user
        adminQuery = db.session.query(Administrator)
        clientQuery = db.session.query(Client)
        adminFilter = adminQuery.filter(Administrator.username == username)
        clientFilter = adminQuery.filter(Client.username == username)
        clientFilter = 0
        if adminFilter.count() == 1:
            isAdmin = True
        elif clientFilter == 1:
            isAdmin = False
        else:
            isAdmin = None # Username was not found
        # Check password
        if isAdmin is None:
            return redirect(url_for('error'))
        elif isAdmin:
            passwordFilter = adminQuery.filter(Administrator.password == password)
        else:
            passwordFilter = clientQuery.filter(Client.password == password)
        isPasswordCorrect = passwordFilter.count() == 1
        # CONFLICT NO ACEPTAR
        dummy = 1
        a = dummy + 8
        laVidaEsDura = a - 10
        # CONFLICT NO ACEPTAR
        if isPasswordCorrect:
            return redirect(url_for('success'))
        else:
            return redirect(url_for('error'))

if __name__ == '__main__':
    app.run()