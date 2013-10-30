"""
Admin interface
"""

from flask import g
from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.sqla import ModelView

from .. import app
from .. import models


class IndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin_index.html')


class BaseAuthModelView(ModelView):
    def is_accessible(self):
        return hasattr(g, "lastuserinfo")

class UserModelView(BaseAuthModelView):
    column_list = ('description', 'fullname', 'email')

class CampaignModelView(BaseAuthModelView):
    column_list = ('name', 'subheading', 'description', 'start', 'end', 'pledged', 'target', 'created_by', 'approved_by', 'approved_on', 'verified_by')

class CategoryModelView(BaseAuthModelView):
    column_list = ('name', 'icon', 'campaigns')


admin = Admin(app, name="Pratham Fundraiser", index_view = IndexView(name="Home"))
admin.add_view(UserModelView(models.User, models.db.session, endpoint = "user"))
admin.add_view(CampaignModelView(models.Campaign, models.db.session, endpoint = "campaign" ))
admin.add_view(CategoryModelView(models.Category, models.db.session, endpoint = "category" ))
# admin.add_view(BaseAuthModelView(models.Image, models.db.session, endpoint = "image" ))







