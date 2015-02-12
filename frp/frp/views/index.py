# -*- coding: utf-8 -*-

import flask

from .. import app
from flask import session, g

from ..models import User



@app.route("/")
def index():
    if session.get('logged_in'):
      g.user = User.query.filter_by(email=session.get('email')).first()
    return flask.render_template('index.html')
