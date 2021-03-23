from flask import Response, request,jsonify
from database.models import Meat, Vegetable
from flask_restful import Resource
import json

# Method for handling API requests related to an item
class ItemApi(Resource):
    def get(self):
        print(type(Meat))
        print(Meat.objects())
        print(type(Meat.objects))
        print(Meat.objects.count())
        query = Meat.objects()
        items = Meat.objects().to_json()
        return Response(items, mimetype="application/json", status=200)