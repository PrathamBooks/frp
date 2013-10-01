import pytest

from flask.ext.lastuser.sqlalchemy import UserManager

from frp import app, lastuser, models

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

