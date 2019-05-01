from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func, Table
from sqlalchemy.orm import relationship, backref
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
    writer = Column(String)
    location = Column(String)
    describe = Column(String)
    
    def __init__(self, writer, location, describe):
        self.writer = writer
        self.location = location
        self.describe = describe

    