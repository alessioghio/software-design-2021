from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

password = "tooga3873"
database = "test"

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:{password}@localhost/{database}"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgres://rxaguhpxsprsvl:4cb9cf7c51e01ba4615f4b1ba2efc27e593cbd07fe751b0109b63d73d6ee5433@ec2-18-214-214-252.compute-1.amazonaws.com:5432/dc5lmvlefddiu5"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class test(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    peopleNum = db.Column(db.Integer)
    message = db.Column(db.Text())
    
    def __init__(self, name, peopleNum, message):
        self.name = name
        self.peopleNum = peopleNum
        self.message = message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['Name']
        peopleNum = request.form['People']
        message = request.form['Message']
        if db.session.query(test).filter(test.name == name).count() == 0:
            data = test(name, peopleNum, message)
            db.session.add(data)
            db.session.commit()
        return render_template('index.html')

if __name__ == '__main__':
    app.run()