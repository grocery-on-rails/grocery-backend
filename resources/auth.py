# Authenticate the user
from os import access
from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import create_access_token
from mongoengine.errors import DoesNotExist
from database.models import User
import datetime

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            User.objects.get(email=body.get('email'))
        except DoesNotExist:
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': str(id)}, 200
        else:
            return {'error': 'Email already exists'}, 409
class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            user = User.objects.get(email=body.get('email'))
        except DoesNotExist:
            return {'error': 'Email not registered'}, 404
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401
        
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        now = datetime.datetime.utcnow()
        expires_epoch = ((now + expires) - datetime.datetime(1970, 1, 1)).total_seconds()
        return {'token': access_token, 'token_expiry': expires_epoch}, 200

        
