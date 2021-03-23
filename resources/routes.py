from .item import ItemsApi, ItemApi

def initialize_routes(api):
    api.add_resource(ItemsApi, '/home')
    api.add_resource(ItemApi, '/product/<id>')