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
    campaigns = Campaign.query.all()
    display_campaigns = []
    if len(campaigns)>=6:
        display_campaigns = filter(lambda x:x.featured==True,campaigns)
        if len(display_campaigns)<6:
            # add other campaigns till the number of campaigns  is 6
            non_featured_campaigns = filter(lambda x:x.featured==False,campaigns)
            i=0
            while len(display_campaigns)<6:
                display_campaigns.append(non_featured_campaigns[i])
                i+=1
    elif len(campaigns)>0:
        # Show the same campaigns again 
        display_campaigns = campaigns
        while len(display_campaigns)<6:
            display_campaigns.append(campaigns[i])
            i+=1

    return flask.render_template('index.html', 
            form=filter_form, 
            total_books_donated=total_books_donated,
            display_campaigns=display_campaigns)

