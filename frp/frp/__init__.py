from flask import Flask
from flask.ext.lastuser import Lastuser
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from ._version import __version__

app = Flask(__name__)
assets = Environment(app)
lastuser = Lastuser()
cache = Cache(app, config = {'CACHE_TYPE' : 'redis'})

css = Bundle("css/bootstrap.css", filters='cssmin', output='gen/all.css')
lib = Bundle("lib/bootstrap/bootstrap.min.js", "lib/angular/angular.js", "lib/angular/angular-route.js", "js/app.js", "js/services.js", "js/controllers.js", "js/filters.js", "js/directives.js", output="gen/lib.js")

assets.register('css_site', css)
assets.register('lib_site', lib)

@app.context_processor
def inject_version():
    return dict(version = __version__,
                testing = app.config.get('LASTUSER_TEST'))

from . import views, models
