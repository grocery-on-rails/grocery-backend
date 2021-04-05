from flask import Response, request
from database.models import Product
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote
from bson import json_util
import json

# Method for handling API requests related to an item
class ItemsApi(Resource):
    def get(self):
        all_products = Product.objects()
        #print(all_products[0:5].to_json())
        recently_viewed = extract_basic_info(json.loads(all_products[0:5].to_json()))
        new_arrivals = extract_basic_info(json.loads(Product.objects()[5:10].to_json()))
        today_deals = extract_basic_info(json.loads(Product.objects()[10:20].to_json()))
        top_sells = extract_basic_info(json.loads(Product.objects()[20:25].to_json()))
        fresh_vegies = extract_basic_info(json.loads(Product.objects()[0:16].to_json()))
        # vegie = json.loads(Vegetable.objects().fields(id=1, name=1, price=1, slice__image_list=1).to_json())
        # #print(Product.objects().)
        data = {}
        data['slides'] = list(["https://via.placeholder.com/150", "https://via.placeholder.com/100", "https://via.placeholder.com/200"])
        data['content'] = list([{'title': 'Recently Viewed', 'content': recently_viewed}, \
        {'title': 'New Arrivals', 'content': new_arrivals}, {'title': 'Today\'s Deals', 'content': today_deals}, \
        {'title': 'Top Sellers', 'content': top_sells}, {'title': 'Fresh Vegies', 'content': fresh_vegies}])
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        new_product =  Product(**body)
        new_product.save()
        id = new_product.id
        return {'id': str(id)}, 200

class ItemApi(Resource):
    def get(self, id):
        item = Product.objects().get(id=id).to_json()
        return Response(item, mimetype="application/json", status=200)

class ItemSearchApi(Resource):
    def get(self, raw_keyword):
        keyword = unquote(raw_keyword)
        pipeline= [
                    {"$search": {"text": {"query": keyword, "path": ["name","subcategory","description","others.quantity"]}}},
                    {"$sort":{"score": -1}},
                    #{"$project": {"_id":0,"name": 1,"price": 1,"score": { "$meta": "searchScore" }}}
                  ]
        matching_products = extract_basic_info((list(Product.objects().aggregate(pipeline))))
        # for product in matching_products:
        #     product["_id"]= {"$oid": str(product["_id"])}
        
        #matching_products = extract_basic_info(json.loads(Product.objects(name__contains=keyword).to_json()))
        print(matching_products)
        return Response(json_util.dumps(matching_products), mimetype="application/json", status=200)

