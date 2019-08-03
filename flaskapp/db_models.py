from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from flaskapp.init_db import Base



class User_info(Base):
    __tablename__ = 'User_info'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    passwd = Column(String)
    name = Column(String)

    def __init__(self, email=None, passwd=None, name='손님', makeSha=False):
        self.email = email
        if makeSha:
            self.passwd = func.sha2(passwd, 256)
        else:
            self.passwd = passwd
        self.name = name
        
    def __repr__(self):
        return 'User %s, %r, %r' % (self.id, self.email, self.name)
        
class Town_record(Base):
    __tablename__ = 'Town_record'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    location = Column(String)
    describe = Column(String)

    def __init__(self, name, title, location, describe):
        self.name = name
        self.title = title
        self.location = location
        self.describe = describe

class File_address(Base):
    __tablename__ = 'File_address'

    id = Column(Integer, primary_key=True)
    card_image = Column(String)

    def __init__(self, card_image):
        self.card_image = card_image
    
        

    