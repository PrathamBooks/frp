import os
import unittest
import tempfile


def test_sample(test_db, test_client):
    "No products added at first"
    op = test_client.get("/")
    assert "No products available" in op.data

def test_add_product(test_db, test_client, last_user):
    "Adding a product to the database"
    test_client.post('/login', data=dict(
        username="noufal",
        password="abcd",
    ), follow_redirects=True)
    op = test_client.get("/product/add")
    print "Hel9"
    print op.data
    
    
    



    
