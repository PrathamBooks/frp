import os

APP_NAME = "Donate-A-Book"

# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://:@localhost/frp"

# Facebook Social Info
FACEBOOK_CONSUMER_KEY=os.environ.get('FACEBOOK_CONSUMER_KEY'),
FACEBOOK_CONSUMER_SECRET=os.environ.get('FACEBOOK_CONSUMER_SECRET')
FACEBOOK_APP_ID=os.environ.get('FACEBOOK_APP_ID')

GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID'),
GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')
SECRET_KEY=os.environ.get('SECRET_KEY')

COST_PER_BOOK=36.75
#DEBUG = True

#ccavenue
CCAVENUE_ACCESS_CODE=os.environ.get('CCAVENUE_ACCESS_CODE')
CCAVENUE_WORKING_KEY=os.environ.get('CCAVENUE_WORKING_KEY')

SITE_NAME="Pratham Books Donate-A-Book"

UPLOAD_DIRECTORY="/home/infodigital/frp/frp/frp/static/uploads"
ALLOWED_EXTENSIONS=set("jpg jpeg png gif JPG JPEG PNG GIF".split())

# Email configuration
MAIL_SERVER = 'localhost'
MAIL_MAILER = '/usr/sbin/sendmail'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL =  False
MAIL_DEBUG = True
MAIL_USERNAME = None
MAIL_PASSWORD =  None
MAIL_DEFAULT_SENDER = DEFAULT_MAIL_SENDER = 'noreply@donateabook.org.in' # Different vars from flask-email and flask-sendmail
MAIL_MAX_EMAILS = None

# Flask-User setting
USER_APP_NAME = APP_NAME
