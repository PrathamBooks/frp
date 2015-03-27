import os

from flask.ext.assets import Environment, Bundle
from ..settings._version import __version__
import logging
from logging.handlers import SMTPHandler
from logging import FileHandler
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from ..models import db


oauth = 0
def init_app(app, settings='settings/development.py'):
    print "Loading config from %s" % settings
    app.config.from_pyfile(settings)
    from .. import views, models

    db.init_app(app)
    db.app = app

    if not app.debug:
        file_handler = FileHandler('server.log')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    app.config['WTF_CSRF_ENABLED'] = False              # Disable CSRF checks while testing

    # Setup Flask-Mail
    mail = Mail(app)

    from ..models import UserAuth, User
    # from app.users.forms import MyRegisterForm
    # from ..views import profile
    db_adapter = SQLAlchemyAdapter(db, User,        # Setup the SQLAlchemy DB Adapter
            UserAuthClass=UserAuth)                 #   using separated UserAuth/User data models
    user_manager = UserManager(db_adapter, app     # Init Flask-User and bind to app
#            register_form=MyRegisterForm,           #   using a custom register form with UserProfile fields
#            user_profile_view_function = profile,
            )
    user_manager.enable_username = False

    assets = Environment(app)

    css = Bundle("css/bootstrap.css",
                 "css/slider.css",
                 "css/fonts.css",
                 "css/jquery-ui.css",
                 "css/prathambooks.css",
                 output='gen/all.css')

    bforms_css = Bundle("css/bootstrap.css",
                 "css/slider.css",
                 "css/bForm.css",
                 "css/jquery-ui.css",
                 output='gen/bforms.css')


    jquery = Bundle("lib/bootstrap/jquery-1.10.2.js", output="gen/jquery.js")
    bootstrap = Bundle("lib/bootstrap/bootstrap.js",
                       "lib/bootstrap/bootstrap-slider.js",
                       output="gen/bootstrap.js")
    angular = Bundle("lib/angular/angular.js",
                     "lib/angular/angular-route.js",
                     output="gen/angular.js")
    underscore = Bundle("lib/underscore/underscore.js",
                        output="gen/underscore.js")
    app_js = Bundle("js/form.js", 
                    "js/donor_form.js",
                    "js/start.js",
                    output="gen/lib.js")

    discover_js = Bundle("js/discover.js", output="gen/discover.js")
    start_js = Bundle("js/start.js", output="gen/start.js")

    assets.register('css_site', css)
    assets.register('bforms', bforms_css)

    assets.register('app_js', app_js)
    assets.register('discover_js', discover_js)
    assets.register('start_js', start_js)
    assets.register('jquery', jquery)
    assets.register('bootstrap', bootstrap)
    assets.register('underscore', underscore)
    assets.register('angular', angular)
