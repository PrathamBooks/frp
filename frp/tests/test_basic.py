import os
import unittest
import tempfile


from frp import app, lastuser, models

def test_sample():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://%s"%tempfile.mktemp()
    app.config['TESTING'] = True
    tc = app.test_client()
    op = tc.get("/")
    print op

    
