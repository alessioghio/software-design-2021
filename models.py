from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import NUMERIC, Boolean, Date, Integer
from database import Manager

class Administrator(Manager.Base):
    __tablename__ = 'administrator'
    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    lastName = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(30), nullable=False)
    userType = Column(VARCHAR(6), nullable=False)

    def __repr__(self):
        return "<Administrator(name=%s, lastName=%s, email=%s, username=%s, password=%s, userType=%s)>".format(
            self.name, self.lastName, self.email, self.username, self.password, self.userType)

class Client(Manager.Base):
    __tablename__ = 'client'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100))
    lastName = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(30), nullable=False)
    userType = Column(VARCHAR(6), nullable=False)
    shoppingCart_id = Column(VARCHAR(100), ForeignKey("shoppingCart.id"), unique=True)

    def __repr__(self):
        return "<Client(name=%s, lastName=%s, email=%s, username=%s, password=%s, userType=%s, id_shoppingCart=%s)>".format(
            self.name, self.lastName, self.email, self.username, self.password, self.userType, self.shoppingCart_id)

class ShoppingCart(Manager.Base):
    __tablename__ = 'shoppingCart'
    id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    client_id = Column(VARCHAR(100), ForeignKey("client.id"), unique=True)
    supply_id = Column(VARCHAR(100), ForeignKey("supply.id"))

    def __repr__(self):
        return "<ShoppingCart(datetime=%s, client_id=%s, supply_id=%s)>".format(
            self.datetime, self.client_id, self.supply_id)

class Supply(Manager.Base):
    __tablename__ = 'supply'
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    price = Column(NUMERIC, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(VARCHAR(100), nullable=False)
    visibility = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Supply(name=%s, price=%s, quantity=%s, category=%s, visibility=%s)>".format(
            self.name, self.price, self.quantity, self.category, self.visibility)

class Recipe(Manager.Base):
    __tablename__ = 'recipe'
    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    quantity = Column(Integer)
    supply_id = Column(BigInteger)

    def __repr__(self):
        return "<Recipe(name=%s, quantity=%s, supply_id=%s)>".format(
            self.name, self.quantity, self.supply_id)

class Transaction(Manager.Base):
    __tablename__ = 'transaction'
    id = Column(BigInteger, primary_key=True, nullable=False)
    datetime = Column(Date, nullable=False)
    unit = Column(VARCHAR(5), nullable=False)
    quantity = Column(Integer, nullable=False)
    supply_id = Column(BigInteger, ForeignKey("supply_id"))
    recipe_id = Column(BigInteger, ForeignKey("recipe_id"))
    admin_id = Column(BigInteger, ForeignKey("admin_id"))
    shoppingCart_id = Column(BigInteger, ForeignKey("shoppingCart_id"))

    def __repr__(self):
        return "<Transaction(datetime=%s, unit=%s, quantity=%s, supply_id=%s, recipe_id=%s, admin_id=%s)>".format(
            self.datetime, self.unit, self.quantity, self.supply_id, self.recipe_id, self.admin_id)

class AdminURL(Manager.Base):
    __tablename__ = 'adminURL'
    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    url = Column(VARCHAR(200))

    def __repr__(self):
        return "<AdminURL(name=%s, url=%s)>".format(
            self.name, self.url)