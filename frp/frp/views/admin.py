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
from ..service.decorators import login_required_admin
from ..service.campaign import get_campaign_rendering_data


class IndexView(AdminIndexView):
    @expose("/")
    @login_required_admin
    def index(self):
        campaign_data = get_campaign_rendering_data()
        return self.render('admin_index.html', campaign_data=campaign_data)


class BaseAuthModelView(ModelView):
    def is_accessible(self):
        return hasattr(g, "lastuserinfo") and g.lastuserinfo



admin = Admin(app, name="Pratham Fundraiser", index_view = IndexView(name="Home"))
admin.add_view(BaseAuthModelView(models.User, models.db.session, endpoint = "user"))
