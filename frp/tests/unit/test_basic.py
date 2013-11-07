import os
import unittest
import tempfile

def test_sample(test_db, test_client):
    "No products added at first"
    op = test_client.get("/")
    assert "No products available" in op.data

   
