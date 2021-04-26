from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import ValidationError
from database.models import User
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote

class UserProfileApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        body = request.get_json()
        if body:    
            if body.get('username'):
                user.username = body.get('username')
            elif body.get('password'):
                user.password = body.get('password')
                user.hash_password()
            elif body.get('email'):
                user.email = body.get('email')
            elif body.get('address'):
                user.address = body.get('address')
            try:
                user.save()
            except ValidationError as e:
                return {'error': str(e)}, 401
            else:
                return {'msg': 'Success'}, 200
        else:
            return {'error': 'Body required'}, 401