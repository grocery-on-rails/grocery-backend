from .item import ItemsApi, ItemApi, ItemSearchApi
from .category import CategoryApi
from .auth import SignupApi, LoginApi
from .cart import CartApi

def initialize_routes(api):
    api.add_resource(ItemsApi, '/home')
    api.add_resource(ItemApi, '/product/<id>')
    api.add_resource(ItemSearchApi, '/search/<raw_keyword>')
    api.add_resource(CategoryApi, '/cat')
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(CartApi, '/cart')