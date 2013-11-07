import sys, os
import pytest

from flask.ext.lastuser.sqlalchemy import UserManager


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../../frp/')

from frp import app, models, lastuser

@pytest.fixture
def test_db(request):
    app.config.from_pyfile("settings/test.py")
    models.db.create_all()
    
@pytest.fixture
def test_client(request):
    app.config.from_pyfile("settings/test.py")
    tc = app.test_client()
    return tc

@pytest.fixture
def last_user(request):
    app.config.from_pyfile("settings/test.py")
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(models.db, models.User))

