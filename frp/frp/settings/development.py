# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://noufal:noufal@localhost/frp"

DEBUG = True
SECRET_KEY = "Development key"

SITE_NAME="Pratham Books Fund raising platform"

UPLOAD_DIRECTORY = "/home/noufal/projects/pratham/pratham_frp/frp/frp/static/uploads"
ALLOWED_EXTENSIONS = set("jpg jpeg png gif".split())

#: LastUser server (frp-auth)
LASTUSER_SERVER = 'http://frp-auth.prathambooks.org/'
LASTUSER_CLIENT_ID = 'z6Ke4mDiSBGxRvBurAvVkQ' 
LASTUSER_CLIENT_SECRET = 'Rxog-fYPQWyHscQL_qGmSg7esBJCHnRoCOYiwfL_bLug'

# Lastuser server (Lastuser.io / localhost)
# LASTUSER_SERVER = 'http://lastuser.io/'
# LASTUSER_CLIENT_ID = 'yhF5SHMIQ5C4ruQJqF9YTQ'   
# LASTUSER_CLIENT_SECRET = 'LTUj8jdtRbCCej_PadT1zQM4cjTdbKTQOkNhDKl-90FA'

# Bypass actual lastuser server 
LASTUSER_TEST = False
