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
    messages = []
    object_name = getattr(typ, "__name__").lower()
    if not hasattr(typ, "verbose_fields"):
        expand = False
        messages.append("Cannot expand '{}' objects".format(object_name))

    matches = []
    if expand:
        for x in data:
            details = x.verbose_fields()
            details['id'] = x.id
            details['url'] = "{}api/v1/{}/{}".format(request.url_root, object_name, x.id)
            matches.append(details)
    else:
        matches = [{'id'  : x.id,
                    'url' : "{}api/v1/{}/{}".format(request.url_root, object_name, x.id)
                    } for x in data]
        
    retval =  dict(item = object_name,
                   expand = expand,
                   matches = matches,
                   messages = messages)
    return retval
    

