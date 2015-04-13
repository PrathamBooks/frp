# -*- coding: utf-8 -*-

import os
from flask import Flask
from .startup.init_app import init_app
app = Flask(__name__)
settings = os.environ.get('FRP_CONFIG', "settings/development.py")
init_app(app=app, settings=settings)

