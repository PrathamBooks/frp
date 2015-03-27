# -*- coding: utf-8 -*-

import flask

from .. import app
from flask import session, g
from ..forms import (FilterForm)

from ..models import User

@app.route("/")
def index():
    filter_form = FilterForm()
    return flask.render_template('index.html', form=filter_form)
