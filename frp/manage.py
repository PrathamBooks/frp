from flask.ext.script import Manager

from frp import app

manager = Manager(app)

@manager.command
def resetdb():
    db = app.models.db
    print "Dropping all tables"
    db.drop_all()
    print "Creating them afresh"
    db.create_all()

if __name__ == '__main__':
    manager.run()

