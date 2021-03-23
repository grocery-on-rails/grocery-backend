from .item import ItemApi
from flask_restful import Resource

def initialize_routes(api):
    api.add_resource(ItemApi, '/api/items')