from flask import Response, request,jsonify
from database.models import Meat, Vegetable
from flask_restful import Resource
import json

# Method for handling API requests related to an item
class ItemsApi(Resource):
    def get(self):
        recently_viewed = json.loads(Meat.objects()[0:5].fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        new_arrivals = json.loads(Meat.objects()[5:10].fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        today_deals = json.loads(Meat.objects()[10:20].fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        top_sells = json.loads(Meat.objects()[20:25].fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        fresh_vegies = json.loads(Vegetable.objects()[0:16].fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        # vegie = json.loads(Vegetable.objects().fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        # #print(Meat.objects().)
        data = {}
        data['slides'] = list(["https://via.placeholder.com/150", "https://via.placeholder.com/100", "https://via.placeholder.com/200"])
        data['content'] = list([{'title': 'recently_viewed', 'content': recently_viewed}, \
        {'title': 'new_arrivals', 'content': new_arrivals}, {'title': 'today_deals', 'content': today_deals}, \
        {'title': 'top_sells', 'content': top_sells}, {'title': 'fresh_vegies', 'content': fresh_vegies}])
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
