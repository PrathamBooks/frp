import os

from flask.ext.script import Manager, Command, Option
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager


from frp import app, models, lastuser

manager = Manager(app)

@manager.command
def runserver(settings = "settings/development.py"):
    """
    Runs the flask development server using the specified config file. 
    
    Defaults to settings/development.py
    """    
    settings = os.environ.get('FRP_CONFIG', settings)
    print "Loading config from %s"%settings
    app.config.from_pyfile(settings)
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(models.db, models.User))
    app.run()

@manager.command
def resetdb(settings = "settings/development.py"):
    app.config.from_pyfile(settings)
    db = models.db
    lastuser = Lastuser()
    print "Dropping all tables"
    db.drop_all()
    print "Creating them afresh"
    db.create_all()
    print "Creating lastuser tables"
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(db, models.User))


if __name__ == '__main__':
    manager.run()

