from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Category, User
from flask_restful import Resource
import time

class OrderPaidApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        new_order = {}
        if user.cart:
            new_order['status'] = 'pending'
            new_order['order_time'] = time.time()
            new_order['delivery_time'] = None
            new_order['address'] = body.get('address')
            new_order['cart'] = user.cart
            user.orders.append(new_order)
            user.cart.clear()
            user.save()
            return {'msg': 'Success'}, 200
        else:
            return {'error': 'User cart is empty'}, 404
