import os
import unittest
import tempfile

from frp import app, lastuser, models

def test_sample(testdb):
    tc = app.test_client()
    op = tc.get("/")
    print op

    
