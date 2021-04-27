from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Product, User
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote
from bson import json_util
import json

class AdminStatsApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        number_customer = User.objects(privilege=False).count()
        number_product = Product.objects().count()
        number_outofstock = Product.objects(stock=0).count()
        number_onsale = Product.objects(discount__ne=0).count()
        number_order = (list(User.objects.aggregate({"$unwind":"$orders"}, {"$count":"number_orders"})))[0]["number_orders"]
        number_belowfive = Product.objects(stock__lte=5).count()
        stats = {'number_customer': number_customer, 'number_product': number_product, 'number_outofstock': number_outofstock, \
                'number_onsale': number_onsale, 'number_order': number_order, 'number_belowfive': number_belowfive}
        return Response(json.dumps(stats), mimetype='json/application', status=200)
        