from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import NUMERIC, Boolean, Date, Integer
from database import Manager
import json

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
        return f"<Administrator(name={self.name}, lastName={self.lastName}, email={self.email}, username={self.username}, password={self.password}, userType={self.userType})>"

class Client(Manager.Base):
    __tablename__ = 'client'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100))
    lastName = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(30), nullable=False)
    cardnumber=Column(VARCHAR(20))
    userType = Column(VARCHAR(6), nullable=False)
    shoppingCart_id = Column(VARCHAR(100), ForeignKey("shoppingCart.id"), unique=True)

    def __repr__(self):
        return f"<Administrator(name={self.name}, lastName={self.lastName}, email={self.email}, username={self.username}, password={self.password}, userType={self.userType}), id_shoppingCart={self.shoppingCart_id})>"

class ShoppingCart(Manager.Base):
    __tablename__ = 'shoppingCart'
    id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    client_id = Column(VARCHAR(100), ForeignKey("client.id"), unique=True)
    supply_id = Column(VARCHAR(100), ForeignKey("supply.id"))
    quantity = Column(Integer)

    def __repr__(self):
        return f"<ShoppingCart(datetime={self.datetime}, client_id={self.client_id}, supply_id={self.supply_id}, quantity={self.quantity})>"

class Supply(Manager.Base):
    __tablename__ = 'supply'
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(500))
    price = Column(NUMERIC, nullable=False)
    quantity = Column(Integer)
    unit = Column(VARCHAR(5), nullable=False)
    category = Column(VARCHAR(100), nullable=False)
    visibility = Column(Boolean, nullable=False)
    admin_id = Column(BigInteger, ForeignKey("administrator.id"), nullable=False)

    def __repr__(self):
        return f"<Supply(name={self.name}, price={self.price}, quantity={self.quantity}, category={self.category}, visibility={self.visibility})>"

class Recipe(Manager.Base):
    __tablename__ = 'recipe'
    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    description = Column(VARCHAR(500))
    quantity = Column(Integer)
    supply_id = Column(BigInteger)
    category = Column(VARCHAR(100), nullable=False)
    price = Column(Integer, nullable=False)
    visibility = Column(Boolean, nullable=False)
    admin_id = Column(BigInteger, ForeignKey("administrator.id"), nullable=False)

    def __repr__(self):
        return f"<Recipe(name={self.name}, quantity={self.quantity}, supply_id={self.supply_id})>"

class Transaction(Manager.Base):
    __tablename__ = 'transaction'
    id = Column(BigInteger, primary_key=True, nullable=False)
    datetime = Column(Date, nullable=False)
    price = Column(NUMERIC, nullable=False)
    admin_id = Column(BigInteger, ForeignKey("administrator.id"))
    client_id = Column(BigInteger, ForeignKey("client.id"))

    def __repr__(self):
        return f"<Transaction(datetime={self.datetime}, unit={self.unit}, quantity={self.quantity}, supply_id={self.supply_id}, recipe_id={self.recipe_id}, admin_id={self.admin_id})>"

class Adminurl(Manager.Base):
    __tablename__ = 'adminurl'
    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    url = Column(VARCHAR(200))
    admin_id = Column(BigInteger, ForeignKey("administrator.id"))

    def __repr__(self):
        return f"<Adminurl(name={self.name}, url={self.url}, admin_id={self.admin_id})>"