from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Category, User
from flask_restful import Resource
from urllib.parse import unquote
from utils.utils import wrap_category_info
import json

class CategoryApi(Resource):
    def get(self):
        all_category = Category.objects()
        categories = json.loads(all_category.to_json())
        data = wrap_category_info(categories)
        return Response(json.dumps(data), mimetype="application/json", status=200)
    
    @jwt_required()
    def post(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        new_cat = Category(**body)
        try:
            new_cat.save()
        except ValidationError:
            return {'error': 'Missing required values or duplicate names'}, 400
        else:
            id = new_cat.id
            return {'id': str(id)}, 200
    
    @jwt_required()
    def delete(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            cat = Category.objects.get(category=body.get('category'))
        except DoesNotExist:
            return {'error': 'Category not found'}, 404
        else:
            cat.delete()
            return {'msg': 'Success'}, 200


class SubcategoryApi(Resource):
    @jwt_required()
    def post(self, raw_keyword):
        cat_name = unquote(raw_keyword)
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            cat = Category.objects.get(category=cat_name)
        except DoesNotExist:
            return {'error': 'Category not found'}, 404
        else:
            body = request.get_json()
            for subcat in body.get('subcategory'):
                cat.subcategory.append(subcat)
            cat.save()
            return {'msg': 'Success'}, 200
    
    @jwt_required()
    def delete(self, raw_keyword):
        cat_name = unquote(raw_keyword)
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            cat = Category.objects.get(category=cat_name)
        except DoesNotExist:
            return {'error': 'Category not found'}, 404
        else:
            body = request.get_json()
            try:
                cat.subcategory.remove(body.get('name'))
            except ValueError:
                return {'error': 'Subcategory not found'}, 404
            else:
                cat.save()
                return {'msg': 'Success'}, 200




