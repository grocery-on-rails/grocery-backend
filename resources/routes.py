from .item import ItemsApi, ItemApi, ItemSearchApi, EmptyStockApi
from .category import CategoryApi, SubcategoryApi
from .auth import SignupApi, LoginApi
from .cart import CartApi
from .usersetting import UserProfileApi

def initialize_routes(api):
    api.add_resource(ItemsApi, '/home')
    api.add_resource(ItemApi, '/product/<id>')
    api.add_resource(ItemSearchApi, '/search/<raw_keyword>')
    api.add_resource(CategoryApi, '/cat')
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(CartApi, '/cart')
    api.add_resource(EmptyStockApi, '/admin/empty')
    api.add_resource(SubcategoryApi, '/cat/<raw_keyword>')
    api.add_resource(UserProfileApi, '/userprofile')