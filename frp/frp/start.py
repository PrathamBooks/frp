import os
from . import app

def start():
    settings = os.environ.get('FRP_CONFIG', "settings/development.py")
    init_app(app=app, settings=settings)
    app.run()
  
