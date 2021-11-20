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

@app.route('/profile-stocker')
def profileAdmin():
    return render_template('profile-stocker.html')  

# ------------------ #

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


# ------ DASHBOARD ADMIN ------ #
from dao.DAOAdmin import DAOAdmin
app.secret_key = 'mysecretkey'
db = DAOAdmin()

@app.route('/user/admin/updatestock')
def index():
    data = db.read(None)
    return render_template('/admintemp/index.html', data=data)

@app.route('/user/admin/updatestock/add')
def add_usuario():
    return render_template('/admintemp/add.html')

@app.route('/user/admin/updatestock/addproduct', methods = ['POST', 'GET'])
def addusuario():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("Nuevo producto creado")
        else:
            flash("ERROR al crear producto")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/user/admin/updatestock/delete/<int:id>')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('admintemp/delete.html', data = data)

@app.route('/user/admin/updatestock/deleteproduct', methods = ['POST'])
def deleteusuario():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('Usuario eliminado')
        else:
            flash('ERROR al eliminar')
        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# ----------------------------- #


if __name__ == '__main__':
    app.run()