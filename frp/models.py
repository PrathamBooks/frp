from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from frp import app

db=SQLAlchemy(app)

class User(db.Model):
    name = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(120))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return "<User %r>\n"%self.name

class Product(db.Model):
    id   = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    description = db.Column(db.String(200))
    user_id = db.Column(db.String, db.ForeignKey("user.name"))
    by = db.relationship('User', 
                         backref = db.backref('user', lazy="dynamic"))
    
    def __init__(self, name, description, user):
        self.name = name
        self.description = description
        self.by = user
        
    def __repr__(self):
        return "<Product %r by %r>"%(self.name, self.by)


        


