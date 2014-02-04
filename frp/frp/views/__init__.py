from .. import app
from . import human, api1

# Enable the API resources.
api1.register_api()
app.register_blueprint(api1.blueprint, url_prefix = "/api/v1/")

