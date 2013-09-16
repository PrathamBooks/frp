from frp import app, lastuser, models

def pytest_funcarg__testdb(request):
    app.config.from_pyfile("settings/test.py")
    models.db.create_all()
    


