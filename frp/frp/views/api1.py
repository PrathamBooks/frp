"""
Implements endpoints for API version 1.
"""

import calendar
import datetime

from flask import Blueprint, make_response, jsonify, abort
from flask.ext.restful import Api, Resource
import markdown

from .. import models

blueprint = Blueprint("apiv1", __name__)
api = Api(blueprint, default_mediatype = "") #, catch_all_404s=True)

def utc_timestamp(d):
    "Converts datetime from UTC to timestamp"
    return calendar.timegm(d.utctimetuple())

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

class Category(Resource):
    def get(self, category_id):
        category = models.Category.query.get(category_id)
        if not category:
            abort(404)        
        return {
            "id": category.id,
            "name" : category.name,
            "icon" : category.icon,
            "campaigns" : [dict(id = campaign.id) 
                           for campaign in category.campaigns]
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
