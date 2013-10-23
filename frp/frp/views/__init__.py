from .. import app
from . import human, api1, admin

# Enable the API resources.
api1.add_resources(api1.routes)
app.register_blueprint(api1.blueprint, url_prefix = "/api/v1/")

