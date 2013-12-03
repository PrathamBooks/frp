from functools import wraps
import calendar

from flask import g, jsonify, make_response, request

from . import app

def allowed_file(fname):
    """
    Returns true if 'fname' has an extension mentioned in
    ALLOWED_EXTENSIONS
    """

    extension = "." in fname and fname.rsplit('.', 1)[-1] or ""
    return extension in app.config['ALLOWED_EXTENSIONS']
        
    
def utc_timestamp(d):
    "Converts datetime from UTC to timestamp"
    return calendar.timegm(d.utctimetuple())
    
def requires_login(f):
    """
    Duplicates the functionality of the lastuser.requires_login but
    doesn't redirect if not authenticated.

    This is necessary to work with API endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.lastuserinfo is None:
            resp = jsonify({"errors" : [
                {"message": "Request was not authenticated"}
            ]})
            resp.headers['WWW-Authenticate'] =  'Oauth realm="Pratham books FRP"'
            return resp, 401
        return f(*args, **kwargs)
    return decorated_function

def create_search_response_v1(data, typ, expand = False):
    """
    Converts a list of results into json that we can send back to the
    client. (API version 1).
    """

    typ = typ.lower()
    if expand:
        matches = [{'id'  : x.id,
                    'url' : "{}api/v1/{}/{}".format(request.url_root, typ, x.id),
                    'other' : 'something'
                    } for x in data]
    else:
        matches = [{'id'  : x.id,
                    'url' : "{}api/v1/{}/{}".format(request.url_root, typ, x.id)
                    } for x in data]
        
    return dict(item = typ,
                matches = matches)
    

