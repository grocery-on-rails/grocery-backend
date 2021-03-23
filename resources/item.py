from flask import Response, request,jsonify
from database.models import Meat, Vegetable
from flask_restful import Resource
import json

# Method for handling API requests related to an item
class ItemsApi(Resource):
    def get(self):
        meat = json.loads(Meat.objects().fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        vegie = json.loads(Vegetable.objects().fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        #print(Meat.objects().)
        data = {}
        data['slides'] = list(["https://via.placeholder.com/150", "https://via.placeholder.com/100", "https://via.placeholder.com/200"])
        data['content'] = list([{'title': 'meat', 'content': meat}, {'title': 'vegetables', 'content': vegie}])
        return Response(json.dumps(data), mimetype="application/json", status=200)
    
    def post(self):
        body = request.get_json()
        new_meat =  Meat(**body)
        new_meat.save()
        id = new_meat.id
        return {'id': str(id)}, 200

class ItemApi(Resource):
    def get(self, id):
        item = json.loads(Meat.objects().get(id=id).to_json())
        print(type(item))
        print(item)
        data = {}
        data['id'] = item['_id']['$oid']
        data['name'] = item['name']
        data['price'] = item['price']
        data['image_list'] = item['image_list']
        data['subcategory'] = item['subcategory']
        data['description'] = item['info_list']
        data['other'] = {
            'unit': item['unit'],
            'quantity': item['quantity'],
            'category': item['category'],
            'country': item['country'],
            'desc': item['desc'],
            'scrapped_url': item['scrapped_url']
            }
        return Response(json.dumps(data), status=200)
