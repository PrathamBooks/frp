from . import human, api1

# Enable the API resources.
api1.add_resources(api1.v1_base_url, api1.routes)
