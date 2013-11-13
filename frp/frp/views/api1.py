"""
Implements endpoints for API version 1.
"""

import calendar
import datetime
import os

from flask import Blueprint, make_response, jsonify, abort, request
from flask.ext.restful import Api, Resource
from flask.views import MethodView
import markdown
from werkzeug import secure_filename


from .. import app, lastuser
from .. import models
from ..models import db
from ..helpers import utc_timestamp, requires_login, allowed_file
from ..forms import CategoryForm

blueprint = Blueprint("apiv1", __name__)
api = Api(blueprint, default_mediatype = "") #, catch_all_404s=True)


class User(Resource):
    def get(self, user_id):
        user = models.User.query.get(user_id)
        if not user:
            abort(404)
        return {
            "id" : user.id,
            "username" : user.username,
            "fullname" : user.fullname,
            "avatar" : user.gravatar(size=20),
            "email" : user.email,
            "twitter" : 'not implemented',
            "authService" : -1,
            "lastLogin" : utc_timestamp(user.updated_at),
            "created" : utc_timestamp(user.created_at),
            "campaigns" : [],
            "currency" : 'not implemented' 
        }


class Campaign(Resource):
    def get(self, campaign_id):
        lat, lon = "10.00N", "25.00E"
        campaign = models.Campaign.query.get(campaign_id)
        if not campaign:
            abort(404)        
        return {
            "id": campaign_id,
            "name" : campaign.name,
            "subheading" : campaign.subheading,
            "brief" : campaign.brief,
            "description" : markdown.markdown(campaign.description),
            "latlng" : "not implemented",
            "gallery" : [dict(heading = image.heading,
                              description = image.description,
                              url = image.url,
                              alt = image.alt,
                              verified = image.verified)
                         for image in campaign.gallery],
            "start" : utc_timestamp(campaign.start),
            "end" : utc_timestamp(campaign.end),
            "pledged" : str(campaign.pledged),
            "target" : str(campaign.target),
            "email" : campaign.created_by.email,
            "twitter" : 'not implemented',
            "authService" : -1,
            "approvedBy" : campaign.approved_by and campaign.approved_by.username or None,
            "approvedOn" : campaign.approved_by and utc_timestamp(campaign.approved_on) or None,
            "verifiedBy" : campaign.verified_by and campaign.verified_by.username or None,
            "verifiedOn" : campaign.verified_by and utc_timestamp(campaign.verified_on) or None,
        }



class Category(MethodView):
    def get(self, category_id):
        print category_id
        category = models.Category.query.get(category_id)
        if not category:
            abort(404)        
        return jsonify({
            "id": category.id,
            "name" : category.name,
            "icon" : category.icon,
            "campaigns" : [dict(id = campaign.id) for campaign in category.campaigns]
        })

    @requires_login    
    def post(self):
        form = CategoryForm()
        if form.validate_on_submit():
            category = models.Category(name = form.name.data)
            icon = request.files['icon']
            filename = secure_filename(icon.filename)
            if filename and allowed_file(filename):
                full_save_path = os.path.join(app.config['UPLOAD_DIRECTORY'], 'icons', filename)
                icon.save(full_save_path)
                category.icon = filename
            db.session.add(category)
            db.session.commit()
            return jsonify({'message' : 'successfully validated'})
        else:
            return jsonify({'message' : 'Error in form'})



class Location(Resource):
    def get(self, location_id):
        lat, lon = "10.00N", "25.00E"
        return {
            "id": location_id,
            "name" : '',
            "photo" : "",#{url},
            "latlng" : [lat, lon],
            "campaigns" : [{}]
        }


def add_resources(resources):
    for resource, url, options in resources:
        api.add_resource(resource, url, **options)

    category = Category.as_view("category")
    blueprint.add_url_rule("category/<int:category_id>", 
                           view_func = category,
                           methods = ["GET"])

    blueprint.add_url_rule("category", 
                           view_func = category,
                           methods = ["POST"])
        
# Tuples of the form (resource, url)
routes = [(User, "user/<int:user_id>", {}),
          (Campaign, "campaign/<int:campaign_id>", {}),          
          # (Category, "category/<int:category_id>", {'methods':['GET']}),
          # (Category, "category/", {'methods':['POST']}),
          (Location, "location/<int:location_id>", {})]


