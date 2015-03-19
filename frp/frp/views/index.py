# -*- coding: utf-8 -*-

import flask

from .. import app
from flask import session, g

from ..models import User

@app.route("/")
def index():
    return flask.render_template('index.html')
