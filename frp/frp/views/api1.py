import calendar
import datetime

from flask.ext.restful import Api, Resource

from .. import app

api = Api(app)

class User(Resource):
    def get(self):
        return {
            "id" : 0,
            "username" : '',
            "firstname" : '',
            "lastname" : '',
            "avatar" : "", #TBD
            "email" : '',
            "twitter" : '',
            "authService" : 0,
            "lastLogin" : calendar.timegm(datetime.datetime.now().utctimetuple()),
            "created" : calendar.timegm(datetime.datetime(2013, 5, 1, 10, 00, 00).utctimetuple()),
            "campaigns" : [],
            "currency" : 'INR'
        }

class Campaign(Resource):
    def get(self):
        lat, lon = "10.00N", "25.00E"
        now = calendar.timegm(datetime.datetime.now().utctimetuple())
        approvedBy = lambda:0 ; approvedBy.id = 10
        verifiedBy = lambda:0 ; verifiedBy.id = 20
        return {
            id: 0,
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
    def get(self):
        return {
            id: 0,
            "name" : '',
            "icon" : 'cssClass',
            "campaigns" : [{}]
        }

class Location(Resource):
    def get(self):
        lat, lon = "10.00N", "25.00E"
        return {
            id: 0,
            "name" : '',
            "photo" : "",#{url},
            "latlng" : [lat, lon],
            "campaigns" : [{}]
        }


def add_resources(base_url, resources):
    for resource, url in resources:
        api.add_resource(resource, 
                         "%s/%s"%(base_url, url))
        
# Tuples of the form (resource, url)
v1_base_url = "/api/v1"
routes = [(User, "user"),
          (Campaign, "campaign"),          
          (Category, "category"),
          (Location, "location")]



