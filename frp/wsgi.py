import os

from frp import app as application

settings = "settings/production.py"
settings = os.environ.get('APP_SETTINGS', settings)

application.config.from_pyfile(settings)
