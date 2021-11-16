from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, ForeignKey
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
        return "<Administrator(name=%s, lastName=%s, email=%s, username=%s, password=%s, userType=%s, id_shoppingCart=%s)>".format(
            self.name, self.lastName, self.email, self.username, self.password, self.userType, self.shoppingCart_id)

class ShoppingCart(Manager.Base):
    __tablename__ = 'shoppingCart'
    id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    client_id = Column(VARCHAR(100), ForeignKey("client.id"), unique=True)
    supply_id = Column(VARCHAR(100), ForeignKey("client.id"))