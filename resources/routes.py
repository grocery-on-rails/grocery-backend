from .item import ItemsApi, ItemApi, ItemSearchApi

def initialize_routes(api):
    api.add_resource(ItemsApi, '/home')
    api.add_resource(ItemApi, '/product/<id>')
    api.add_resource(ItemSearchApi, '/search/<keyword>')