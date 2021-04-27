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
        pipeline=[{"$unwind": "$orders" },{"$unwind": "$orders.cart" },{"$group":{"_id":"$orders.cart.product_id", "quantity":{"$sum": "$orders.cart.quantity"}}}, {"$sort":{"quantity":-1}}]
        result=list(User.objects.aggregate(pipeline))
        sales=[json.loads(Product.objects(id=i["_id"])[0].to_json()) for i in result]
        for i,pro in enumerate(sales):
            pro["stock"]=result[i]["quantity"]
        top_sells = extract_basic_info(sales)
        stats = {'number_customer': number_customer, 'number_product': number_product, 'number_outofstock': number_outofstock, \
                'number_onsale': number_onsale, 'number_order': number_order, 'number_belowfive': number_belowfive, "top_sells":top_sells}
        return Response(json.dumps(stats), mimetype='json/application', status=200)
        