# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://alok:alok@localhost/frp"

DEBUG = True
SECRET_KEY = "Development key"

SITE_NAME="Pratham Books Fund raising platform"

#: LastUser server
LASTUSER_SERVER = 'http://frp-auth.prathambooks.org'
#: LastUser client id
LASTUSER_CLIENT_ID = 'FUVs_77tS9S4wHl0DVvkqQ'
#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'DKERE5jARl6bcnjo68e7EQDRI5XwCeTz6_3p4ly96oMA'

# Bypass actual lastuser server 
LASTUSER_TEST = False
