"""
Admin interface
"""

from flask import g
from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import BaseForm

from wtforms import TextField
from wtforms.validators import DataRequired

from .. import app
from .. import models


class IndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin_index.html')


class BaseAuthModelView(ModelView):
    def is_accessible(self):
        return hasattr(g, "lastuserinfo") and g.lastuserinfo
    
    

admin = Admin(app, name="Pratham Fundraiser", index_view = IndexView(name="Home"))
admin.add_view(BaseAuthModelView(models.User, models.db.session, endpoint = "user"))
admin.add_view(BaseAuthModelView(models.Campaign, models.db.session, endpoint = "campaign" ))
admin.add_view(BaseAuthModelView(models.Category, models.db.session, endpoint = "category" ))
admin.add_view(BaseAuthModelView(models.Image, models.db.session, endpoint = "image" ))







