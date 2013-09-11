from flask import Flask
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager


from frp import app, lastuser, models

import settings

if __name__ == "__main__":
    app.config.from_object(settings)
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(models.db, models.User))
    app.run(debug=True)
