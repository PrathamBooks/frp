"""
Admin interface
"""

from .. import app
from .. import models
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView


admin = Admin(app, name="Pratham Fundraiser")
admin.add_view(ModelView(models.User, models.db.session))
admin.add_view(ModelView(models.Product, models.db.session))







