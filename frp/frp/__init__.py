from flask import Flask
from flask.ext.lastuser import Lastuser
from ._version import __version__

app = Flask(__name__)
lastuser = Lastuser()

@app.context_processor
def inject_version():
    return dict(version=__version__)


from . import views, models
