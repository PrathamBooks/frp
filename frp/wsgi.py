import os

from frp import app as application
from frp.models import db

db.init_app(application)
db.app = application
db.create_all()

settings = "settings/production.py"
settings = os.environ.get('APP_SETTINGS', settings)

application.config.from_pyfile(settings)
