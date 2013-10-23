# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://noufal:noufal@localhost/frp"

DEBUG = True
SECRET_KEY = "Development key"

SITE_NAME="Pratham Books Fund raising platform"

#: LastUser server
LASTUSER_SERVER = 'http://frp-auth.prathambooks.org/'
#: LastUser client id
LASTUSER_CLIENT_ID = 'z6Ke4mDiSBGxRvBurAvVkQ'
#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'Rxog-fYPQWyHscQL_qGmSg7esBJCHnRoCOYiwfL_bLug'

# Bypass actual lastuser server 
LASTUSER_TEST = True
