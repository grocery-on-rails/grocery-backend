from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Category, User
from flask_restful import Resource
from bson import json_util
import time

class OrderPaidApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        new_order = {}
        if user.cart:
            order_created = time.time()
            new_order['order_id'] = str(user_id) + str(order_created)
            new_order['status'] = 'pending'
            new_order['order_time'] = order_created
            new_order['delivery_time'] = None
            new_order['address'] = body.get('address')
            new_order['cart'] = user.cart
            new_order['payment_method'] = body.get('payment_method')
            user.orders.append(new_order)
            user.cart = None
            user.save()
            return {'msg': 'Success'}, 200
        else:
            return {'error': 'User cart is empty'}, 404
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if user.orders:
            return Response(json_util.dumps(user.orders), mimetype="json/application", status=200)
        else:
            return {'error': 'User has no orders'}, 404

class RetrieveOrdersApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        users = User.objects(orders__0__exists=True).only('username', 'email', 'orders').to_json()
        return Response(users, mimetype="json/application", status=200)
