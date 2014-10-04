#!/usr/bin/env python

import datetime
import os
import subprocess

from flask.ext.script import Manager

from frp import app
from frp.models import db

manager = Manager(app)
db.init_app(app)
db.app = app

settings = "settings/development.py"
test_settings = "settings/testing.py"
settings = os.environ.get('FRP_CONFIG', settings)
print "Loading config from %s" % settings


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


@manager.command
def gendata():
    """
    Creates a few campaigns that we can use to run our tests on.
    """
    app.config.from_pyfile(settings)
    lastuser.init_app(app)
    user = models.User.query.all()[0]
    for i in range(1, 100):
        m = models.Campaign(name = "campaign-{}".format(i),
                            subheading = "Subheading {}".format(i),
                            brief = subprocess.Popen("/usr/games/fortune -s".split(), stdout = subprocess.PIPE).stdout.read(),
                            description = subprocess.Popen("/usr/games/fortune -l".split(), stdout = subprocess.PIPE).stdout.read(),
                            latitude = i,
                            latitude_hem = "N",
                            longitude = i,
                            longitude_hem = "E",
                            start = datetime.datetime.now(),
                            end = datetime.datetime.now() + datetime.timedelta(days = 10),
                            created_by = user)
        models.db.session.add(m)
    models.db.session.commit()


@manager.command
def resetdb():
    global settings
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
