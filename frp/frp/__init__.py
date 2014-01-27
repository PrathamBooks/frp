from flask import Flask
from flask.ext.lastuser import Lastuser
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from ._version import __version__
from .mailer import Mailer

app = Flask(__name__)
assets = Environment(app)
lastuser = Lastuser()
mailer = Mailer(app)
cache = Cache(app, config = {'CACHE_TYPE' : 'redis'})

css = Bundle("css/bootstrap.css",
             # "css/bootstrap-theme.min.css",
             "css/slider.css",
             output='gen/all.css')

jquery = Bundle("lib/bootstrap/jquery-1.10.2.js", output="gen/jquery.js")
bootstrap = Bundle("lib/bootstrap/bootstrap.min.js", "lib/bootstrap/bootstrap-slider.js", output="gen/bootstrap.js")
angular = Bundle("lib/angular/angular.js", "lib/angular/angular-route.js", output="gen/angular.js")
app_js = Bundle("js/tmp/form.js", output="gen/lib.js")


# app_js = Bundle("js/app.js",
#                 "js/services.js",
#                 "js/controllers.js",
#                 "js/filters.js",
#                 "js/directives.js",
#                 output="gen/lib.js")

assets.register('css_site', css)

assets.register('app_js', app_js)
assets.register('jquery', jquery)
assets.register('bootstrap', bootstrap)
assets.register('angular', angular)



@app.context_processor
def inject_version():
    return dict(version = __version__,
                testing = app.config.get('LASTUSER_TEST'))

from . import views, models
