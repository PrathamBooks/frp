# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://noufal:noufal@localhost/frp"

DEBUG = True
SECRET_KEY = "Development key"

SITE_NAME="Pratham Books Fund raising platform"

#: LastUser server
LASTUSER_SERVER = 'http://frp-auth.prathambooks.org/'
# LASTUSER_SERVER = 'http://lastuser.io/'
#: LastUser client id
LASTUSER_CLIENT_ID = 'z6Ke4mDiSBGxRvBurAvVkQ' # frp-auth client id
# LASTUSER_CLIENT_ID = 'yhF5SHMIQ5C4ruQJqF9YTQ'   # lastuser.io client id

#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'Rxog-fYPQWyHscQL_qGmSg7esBJCHnRoCOYiwfL_bLug'
# LASTUSER_CLIENT_SECRET = 'LTUj8jdtRbCCej_PadT1zQM4cjTdbKTQOkNhDKl-90FA'

# Bypass actual lastuser server 
LASTUSER_TEST = False
