from .item import ItemApi

def initialize_routes(api):
    api.add_resource(ItemApi, '/api/items')