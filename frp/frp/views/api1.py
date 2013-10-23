"""
Implements endpoints for API version 1.
"""

import calendar
import datetime

from flask import Blueprint, make_response, jsonify, abort
from flask.ext.restful import Api, Resource

from .. import models

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
            "lastLogin" : calendar.timegm(user.updated_at.utctimetuple()),
            "created" : calendar.timegm(user.created_at.utctimetuple()),
            "campaigns" : [],
            "currency" : 'not implemented' 
        }

class Campaign(Resource):
    def get(self, campaign_id):
        lat, lon = "10.00N", "25.00E"
        now = calendar.timegm(datetime.datetime.now().utctimetuple())
        approvedBy = lambda:0 ; approvedBy.id = 10
        verifiedBy = lambda:0 ; verifiedBy.id = 20
        return {
            "id": campaign_id,
            "name" : '',
            "subheading" : '',
            "brief" : '',
            "description" : '<html>',
            "latlng" : [lat, lon],
            "gallery" : [{
                "heading" : '',
                "description" : '',
                "url" : "", #{url},
                "alt" : '',
                "verified" : True
            }],
           "start" : now,
            "end" : now,
            "pledged" : 0,
            "target" : 0,
            "email" : '',
            "twitter" : '',
            "authService" : 0,
            "approvedBy" : approvedBy.id,
            "approvedOn" : now,
            "verifiedBy" : verifiedBy.id,
            "verifiedOn" : now,
        }

class Category(Resource):
    def get(self, category_id):
        return {
            "id": category_id,
            "name" : '',
            "icon" : 'cssClass',
            "campaigns" : [{}]
        }

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
    for resource, url in resources:
        api.add_resource(resource, url)

        
# Tuples of the form (resource, url)
routes = [(User, "user/<int:user_id>"),
          (Campaign, "campaign/<int:campaign_id>"),          
          (Category, "category/<int:category_id>"),
          (Location, "location/<int:location_id>")]
