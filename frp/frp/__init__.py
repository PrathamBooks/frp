# -*- coding: utf-8 -*-

from flask import Flask
from .startup.init_app import init_app
app = Flask(__name__)
init_app(app)

