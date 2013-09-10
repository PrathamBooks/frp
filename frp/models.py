from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.lastuser.sqlalchemy import UserBase

from frp import app

db=SQLAlchemy(app)

class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)


# --- Models ------------------------------------------------------------------

class User(UserBase, db.Model):
    __tablename__ = 'user'
    description = db.Column(db.Text, default=u'', nullable=False)

    def __repr__(self):
        return "<User %r>\n"%self.username

class Product(db.Model):
    id   = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    by = db.relationship('User', 
                         backref = db.backref('user', lazy="dynamic"))
    
    def __init__(self, name, description, user):
        self.name = name
        self.description = description
        self.by = user
        
    def __repr__(self):
        return "<Product %r by %r>"%(self.name, self.by)


        


