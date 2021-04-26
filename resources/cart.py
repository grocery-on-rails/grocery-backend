from re import I
from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist
from database.models import Product, User
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote
from bson import json_util
import json

class CartApi(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        product_id = body.get('product_id')
        quantity = body.get('quantity')
        if quantity == 0:
            try:
                user = User.objects.get(id=user_id, cart__product_id=product_id)
            except DoesNotExist:
                return {'error': 'Trying to delete an item that is not in the cart'}, 404
            else:
                for i in range(len(user.cart)):
                    item = user.cart[i]
                    if item['product_id'] == product_id:
                        index = i
                        break
                user.cart.pop(index)
                user.save()
                return {'msg': 'Success'}, 200
        else:
            try:
                user = User.objects.get(id=user_id, cart__product_id=product_id)
            except DoesNotExist:
                user = User.objects.get(id=user_id)
                new_dict = {"product_id": product_id, "quantity": quantity}
                if user.cart:
                    user.cart.append(new_dict)
                else:
                    user.cart = [new_dict]
            else:
                for item in user.cart:
                    if(item['product_id'] == product_id):
                        item['quantity'] = quantity
            user.save()
            return {'msg': 'Success'}, 200
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        cart_items_with_quantity = []
        invalid_item_index = []
        cnt = 0
        for item in user.cart:
            try:
                cart_item = json.loads(Product.objects.get(id=item['product_id']).to_json())
            except DoesNotExist:
                invalid_item_index.append(cnt)
            else:    
                cart_items_with_quantity.append({'product_summary': extract_basic_info(cart_item), 'quantity': item['quantity']})
            cnt+=1
        if invalid_item_index:
            for x in reversed(invalid_item_index):
                user.cart.pop(x)
            user.save()
        return Response(json.dumps(cart_items_with_quantity), mimetype="application/json", status=200)
