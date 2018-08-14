from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from passlib.hash import pbkdf2_sha256


Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), index=True, unique=True)
    name = Column(String(20), index=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)


# engine that stores data in the lcoal directory's
# sqlalchemy example.db file;
engine = create_engine('sqlite:///app.db')

# create all tables in the engine
Base.metadata.create_all(engine)
