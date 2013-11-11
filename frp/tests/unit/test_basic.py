import os
import unittest
import tempfile
from frp import app, lastuser

def test_sample(test_db, test_client):
    "No products added at first"
    op = test_client.get("/")
    assert "No products available" in op.data

def test_add_product(test_db, test_client, last_user):
    "Adding a product to the database"
    app.lastuser_auth_data = dict(
        token_scope = u'name email',
        userid = u'1', 
        username = u'alokk', 
        email = u'kuchlous@gmail.com', 
        fullname = u'Alok Kuchlous'
        )
    app.lastuser_auth_token = dict(
        access_token = u'pAfGGWHzRtqRmdSQ_CdrWA',
        token_type = u'bearer',
        scope = u'email id')

    op = test_client.get("/product/add", follow_redirects=True)
    assert "Create new product" in op.data   
