# -*- coding: utf-8 -*-

import flask

from .. import app
from flask import session, g
from ..forms import (FilterForm)

from ..models import User, Donation,Campaign

@app.route("/")
def index():
    filter_form = FilterForm()
    total_books_donated = Donation.total_books_donated
    display_campaigns = Campaign.query.filter_by(featured=True).filter_by(status='Approved').limit(6).all()
    if len(display_campaigns)<6:
        # add other campaigns to make 6
        more_campaigns_needed = 6 - len(display_campaigns)
        non_featured_campaigns = Campaign.query.filter_by(featured=False).filter_by(status='Approved').limit(more_campaigns_needed).all()
        display_campaigns = display_campaigns + non_featured_campaigns
    # if still not enough just repeat the first
    if len(display_campaigns)<6 and len(display_campaigns)>0:
        while len(display_campaigns)<6:
            display_campaigns = display_campaigns + display_campaigns

    return flask.render_template('index.html', 
            form=filter_form, 
            total_books_donated=total_books_donated,
            display_campaigns=display_campaigns)
