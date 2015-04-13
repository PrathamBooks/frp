# -*- coding: utf-8 -*-

import flask

from .. import app
from flask import session, g
from ..forms import (FilterForm)

from ..models import User, Donation

@app.route("/")
def index():
    filter_form = FilterForm()
    total_books_donated = Donation.total_books_donated
    return flask.render_template('index.html', 
            form=filter_form, 
            total_books_donated=total_books_donated)
