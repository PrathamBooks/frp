import os

from flask_assets import Environment, Bundle
from ..settings._version import __version__
import logging
from logging.handlers import SMTPHandler
from logging import FileHandler
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from ..models import db
import jinja2
import flask_excel as excel

_js_escapes = {
        '\\': '\\u005C',
        '\'': '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        u'\u2028': '\\u2028',
        u'\u2029': '\\u2029'
}
# Escape every ASCII character with a value less than 32.
_js_escapes.update(('%c' % z, '\\u%04X' % z) for z in xrange(32))

def jinja2_escapejs_filter(value):
        retval = []
        for letter in value:
                if _js_escapes.has_key(letter):
                        retval.append(_js_escapes[letter])
                else:
                        retval.append(letter)

        return jinja2.Markup("".join(retval))

def init_app(app, settings='settings/development.py'):
    print "Loading config from %s" % settings
    app.config.from_pyfile(settings)
    from .. import views, models

    db.init_app(app)
    db.app = app
    excel.init_excel(app)

    if not app.debug:
        file_handler = FileHandler('server.log')
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.config['WTF_CSRF_ENABLED'] = False              # Disable CSRF checks while testing
    app.config['VERSION'] = __version__

    # Setup Flask-Mail
    mail = Mail(app)

    from ..models import UserAuth, User
    # from app.users.forms import MyRegisterForm
    # from ..views import profile
    db_adapter = SQLAlchemyAdapter(db, User,        # Setup the SQLAlchemy DB Adapter
            UserAuthClass=UserAuth)                 #   using separated UserAuth/User data models
    user_manager = UserManager(db_adapter, app     # Init Flask-User and bind to app
            )
    user_manager.enable_username = False
    user_manager.after_register_endpoint = 'after_register'
    user_manager.password_validator = lambda x, y: True

    assets = Environment(app)

    css = Bundle("css/bootstrap.css",
                 "css/slider.css",
                 "css/fonts.css",
                 "css/prathambooks.css",
		 filters="cssmin",
                 output='gen/all.css')

    underscore = Bundle("lib/underscore/underscore.js",
                        output="gen/underscore.js")

    app_js = Bundle("js/form.js", 
                    "js/donor_form.js",
                    "js/start.js",
                    "js/admin.js",
                    "js/admin_graphs.js",
                    "js/discover.js",
                    "js/utils.js",
                    "js/tablesorter.js",
                    "lib/bootstrap/bootstrap.file-input.js",
                    "js/responsive-tabs.js",
                    filters="jsmin",
                    output="gen/lib.js")

    assets.register('css_site', css)
    assets.register('app_js', app_js)
    assets.register('underscore', underscore)
    app.jinja_env.filters['escapejs'] = jinja2_escapejs_filter
