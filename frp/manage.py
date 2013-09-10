from flask.ext.script import Manager
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager


import models
from frp import app

manager = Manager(app)

@manager.command
def resetdb():
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

