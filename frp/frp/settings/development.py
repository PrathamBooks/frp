import os

# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://:@localhost/frp"

# Facebook Social Info

FACEBOOK_CONSUMER_KEY = os.environ.get('FACEBOOK_CONSUMER_KEY'),
FACEBOOK_CONSUMER_SECRET =  os.environ.get('FACEBOOK_CONSUMER_SECRET')

DEBUG = True
SECRET_KEY = "Development key"

SITE_NAME="Pratham Books Fund raising platform"

UPLOAD_DIRECTORY = "/home/noufal/projects/pratham/pratham_frp/frp/frp/static/uploads"
ALLOWED_EXTENSIONS = set("jpg jpeg png gif".split())

# Email configuration
MAIL_SERVER = 'localhost'
MAIL_MAILER = '/usr/sbin/sendmail'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL =  False
MAIL_DEBUG = True
MAIL_USERNAME = None
MAIL_PASSWORD =  None
MAIL_DEFAULT_SENDER = DEFAULT_MAIL_SENDER = 'noufal@localhost.localdomain' # Different vars from flask-email and flask-sendmail
MAIL_MAX_EMAILS = None
