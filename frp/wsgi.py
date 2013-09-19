from flask.ext.lastuser.sqlalchemy import UserManager
from frp import app, models, lastuser

settings="settings/development.py"

app.config.from_pyfile(settings)
lastuser.init_app(app)
lastuser.init_usermanager(UserManager(models.db, models.User))

