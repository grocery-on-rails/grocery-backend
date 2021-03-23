from flask import Response, request
from database.models import Meat, Vegetable
from flask_restful import Resource

# Method for handling API requests related to an item
class ItemApi(Resource):
    def get(self):
        query = Meat.objects()
        items = Meat.objects().to_json()
        return Response(items, mimetype="application/json", status=200)