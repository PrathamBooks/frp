import os

from frp import app

settings = "settings/production.py"
settings = os.environ.get('FRP_CONFIG', settings)

app.config.from_pyfile(settings)
