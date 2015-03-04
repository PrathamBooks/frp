# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from ._version import __version__
from .mailer import Mailer


def create_app(settings='settings/development.py'):
    app = Flask(__name__)
    app.config.from_pyfile(settings)
    return app

app = create_app(
    os.environ.get('APP_SETTINGS', 'settings/development.py'))

import logging
from logging import FileHandler
file_handler = FileHandler('server.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

assets = Environment(app)

mailer = Mailer(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

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
app_js = Bundle("js/form.js", output="gen/lib.js")
discover_js = Bundle("js/discover.js", output="gen/discover.js")


assets.register('css_site', css)
assets.register('bforms', bforms_css)

assets.register('app_js', app_js)
assets.register('discover_js', discover_js)
assets.register('jquery', jquery)
assets.register('bootstrap', bootstrap)
assets.register('angular', angular)


from . import views, models
