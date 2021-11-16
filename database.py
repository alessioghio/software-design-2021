from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Developermust create a file named dbCredentials.py and insert the local name 
# of database and password. This file is included in the .gitignore so people's
# credentials are not mixed
from dbCredentials import database, password

class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self, ENV):
        if ENV == 'dev':
            engine = create_engine(f"postgresql://postgres:{password}@localhost/{database}", echo=False)
        else:
            engine = create_engine(f"postgresql://rxaguhpxsprsvl:4cb9cf7c51e01ba4615f4b1ba2efc27e593cbd07fe751b0109b63d73d6ee5433@ec2-18-214-214-252.compute-1.amazonaws.com:5432/dc5lmvlefddiu5", echo=False)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()
        return session
