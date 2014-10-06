#!/usr/bin/env python

import datetime
import os
import subprocess

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from frp import app
from frp.models import db

manager = Manager(app)
db.init_app(app)
db.app = app

settings = "settings/development.py"
test_settings = "settings/testing.py"
settings = os.environ.get('APP_SETTINGS', settings)
print "Loading config from %s" % settings


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    """
    Runs the flask development server using the specified config file.

    Defaults to settings/development.py
    """
    global settings
    app.config.from_pyfile(settings)
    db.create_all()
    app.run()


# @manager.command
# def migrate():
#     """
#     Runs alembic migration
#     """
#     global settings
#     app.config.from_pyfile(settings)
#     db.create_all()
#     ManageMigrations().run()


@manager.command
def resetdb():
    global settings, db
    app.config.from_pyfile(settings)
    print "Dropping all tables"
    db.drop_all()
    print "Creating them afresh"
    db.create_all()
    print "Creating lastuser tables"


if __name__ == '__main__':
    manager.run()
