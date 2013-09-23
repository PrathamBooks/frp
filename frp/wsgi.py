import os

from flask.ext.lastuser.sqlalchemy import UserManager
from frp import app, models, lastuser

settings="settings/production.py"
settings = os.environ.get('FRP_CONFIG', settings)

app.config.from_pyfile(settings)
lastuser.init_app(app)
lastuser.init_usermanager(UserManager(models.db, models.User))

