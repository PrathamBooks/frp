from functools import wraps
import calendar

from flask import g

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
            return {"errors" : [
                {"message": "Request was not authenticated"}
            ]}, 401, {'WWW-Authenticate' : 'Oauth realm="Pratham books FRP"'}
        return f(*args, **kwargs)
    return decorated_function
