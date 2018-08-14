from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from model.py which shows my models
from model import User, Base

engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
#DBSession.bind = engine do this when engine isn't crreated already
session = DBSession()
