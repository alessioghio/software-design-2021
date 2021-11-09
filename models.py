from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# , unique=True

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    lastName = db.Column(db.VARCHAR(100), nullable=False)
    email = db.Column(db.VARCHAR(100), nullable=False)
    username = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.VARCHAR(30), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity':'user',
    }
    def __init__(self, name, lastName, email, username, password):
        self.name = name
        self.lastName = lastName
        self.email = email
        self.username = username
        self.password = password

class Administrator(User):
    __tablename__ = 'administrator'
    __mapper_args__ = {
        'polymorphic_identity':'administrator',
    }

class Client(User):
    __tablename__ = 'administrator'
    shoppingCart_id = db.Column(db.ForeignKey('shoppingCart.id'))
    __mapper_args__ = {
        'polymorphic_identity':'client',
    }

class Supply(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.VARCHAR(100), nullable=False)
    visibility = db.Column(db.Boolean, nullable=False)
    def __init__(self, idSupply, name, price, unidad, quantity, category, visibility):
        self.idSupply = idSupply
        self.name = name
        self.price = price
        # self.unidad = unidad
        # self.unidad = unidad
        self.quantity = quantity
        self.category = category
        self.visibility = visibility