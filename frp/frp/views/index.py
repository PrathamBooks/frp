# -*- coding: utf-8 -*-

import flask

from .. import app


@app.route("/")
def index():
    return flask.render_template('index.html')
