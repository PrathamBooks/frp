import os

APP_NAME = "Donate-A-Book"

# Database settings
SQLALCHEMY_DATABASE_URI = "postgresql://:@localhost/frp"

# Facebook Social Info

FRP_FACEBOOK_APP_ID=687940051328349
FRP_SECRET='4e753f463175c5f7aaf01a4c1ae4ce91'
FACEBOOK_APP_ID='828919617156016'
MY_FACEBOOK_APP_SECRET='cccd507c38517c64cfe3f38b048ce2d9'
MY_FACEBOOK_TEST_APP_ID=828920413822603
MY_FACEBOOK_TEST_APP_SECRET='28d234cea81bbd081f956f86a3d15e73'

FACEBOOK_APP_ID=os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_CONSUMER_KEY = os.environ.get('FACEBOOK_CONSUMER_KEY'),
FACEBOOK_CONSUMER_SECRET =  os.environ.get('FACEBOOK_CONSUMER_SECRET')

GOOGLE_CLIIENT_ID='333461527138-5uefjj1d3u859ca68f9huv3n3sp2cfnr.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET='NvAEJHMsjN3rT8y5UVXyvfNv'

DEBUG = True
SECRET_KEY = "Development key"
OLD_COST_PER_BOOK=36.75
COST_PER_BOOK=40

SITE_NAME="Pratham Books Donate-A-Book"

UPLOAD_DIRECTORY = "/home/alokk/frp/frp/frp/static/uploads"
ALLOWED_EXTENSIONS = set("jpg jpeg png gif JPG JPEG PNG GIF".split())

# Email configuration
MAIL_SERVER = 'localhost'
MAIL_MAILER = '/usr/sbin/sendmail'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL =  False
MAIL_DEBUG = True
MAIL_USERNAME = None
MAIL_PASSWORD =  None
MAIL_DEFAULT_SENDER = DEFAULT_MAIL_SENDER = 'frp@ec2-52-74-2-167.ap-southeast-1.compute.amazonaws.com' # Different vars from flask-email and flask-sendmail
MAIL_MAX_EMAILS = None

# Flask-User setting
USER_APP_NAME = APP_NAME
