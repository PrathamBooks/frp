import sys
import os
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../../frp/')

from frp import app, models


@pytest.fixture
def test_db(request):
    app.config.from_pyfile("settings/test.py")
    models.db.create_all()
    def fin():
        models.db.drop_all()
    request.addfinalizer(fin)

@pytest.fixture
def test_client(request):
    app.config.from_pyfile("settings/test.py")
    tc = app.test_client()
    return tc
