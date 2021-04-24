from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Product, User
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote
from bson import json_util
import json


# Method for handling API requests related to an item
class ItemsApi(Resource):
    def get(self):
        all_products = Product.objects()
        recently_viewed = extract_basic_info(json.loads(all_products[0:5].to_json()))
        new_arrivals = extract_basic_info(json.loads(Product.objects()[5:10].to_json()))
        today_deals = extract_basic_info(json.loads(Product.objects(discount__gt=0)[:20].to_json()))
        top_sells = extract_basic_info(json.loads(Product.objects()[20:25].to_json()))
        fresh_vegies = extract_basic_info(json.loads(Product.objects()[0:16].to_json()))
        data = {}
        data['slides'] = list(["https://via.placeholder.com/150", "https://via.placeholder.com/100", "https://via.placeholder.com/200"])
        data['content'] = list([{'title': 'Recently Viewed', 'content': recently_viewed}, \
        {'title': 'New Arrivals', 'content': new_arrivals}, {'title': 'Today\'s Deals', 'content': today_deals}, \
        {'title': 'Top Sellers', 'content': top_sells}, {'title': 'Fresh Vegies', 'content': fresh_vegies}])
        return Response(json.dumps(data), mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            new_product = Product(**body)
        except ValidationError:
            return {'error': 'Missing required values'}, 400
        else:
            new_product.save()
            id = new_product.id
            return {'id': str(id)}, 200
    
    @jwt_required()
    def delete(self):
        body = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            item = Product.objects.get(id=body.get('id'))
        except DoesNotExist:
            return {'error': 'Product not found'}, 404
        item.delete()
        return {'msg': 'Success'}, 200

class ItemApi(Resource):
    def get(self, id):
        try:
            item = Product.objects().get(id=id).to_json()
        except DoesNotExist:
            return {'error': 'Product ID not found'}, 404
        else:
            return Response(item, mimetype="application/json", status=200)
    
    @jwt_required()
    def post(self, id):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        try:
            item = Product.objects.get(id=id)
        except DoesNotExist:
            return {'error': 'Product ID not found'}, 404
        else:
            body = request.get_json()
            for field in ['name', 'price', 'image_list', 'subcategory', 'description', 'scraped_url', 'stock', 'discount']:
                if body.get(field):
                    item[field] = body.get(field)
            item.save()
            return {'msg': 'Success'}, 200

class ItemSearchApi(Resource):
    @jwt_required(optional=True)
    def get(self, raw_keyword):
        user_id = get_jwt_identity()
        isAdmin = False
        if user_id:
            user = User.objects.get(id=user_id)
            if user.privilege:
                isAdmin = True

        body = request.get_json()

        isSortByPrice = True
        isAscending = True
        if body.get('sort') == 'price+':
            pass
        elif body.get('sort') == 'price-':
            isAscending = False
        else:
            isSortByPrice = False
            isAscending = False
        match={"$match":{}}
        price_min  = 0
        price_max = 999999
        if body.get('price_min'):
            price_min = int(body.get('price_min'))
            match["$match"]["price"]={"$gte":price_min}
        if body.get('price_max'):
            price_max = int(body.get('price_max'))
            match["$match"]["price"]={"$lte":price_max}
        
        list_subcategory = []
        if body.get('subcategories'):
            list_subcategory = body.get('subcategories')
            match["$match"]["subcategory"]={"$all":list_subcategory}


        keyword = unquote(raw_keyword)
        pipeline= [  
                    {"$search": {"text": {"query": keyword, "path": ["name","subcategory","description","others.quantity"]}}},
                    
                    {"$sort":{"score"*(1-int(isSortByPrice))+"price"*(int(isSortByPrice)): -1+2*(int(isAscending))}},
                    #{"$project": {"_id":0,"name": 1,"price": 1,"score": { "$meta": "searchScore" }}}
                  ]
        if len(match["$match"])!=0:
            pipeline.insert(1,match)
        print(pipeline)
        matching_products = extract_basic_info((list(Product.objects().aggregate(pipeline))), isAdmin)[:100]
        ids=[str(i["_id"]) for i in matching_products]
       
        if len(matching_products)<10:
                kwargs = dict(name__istartswith=keyword, price__gte=price_min,price__lte=price_max, subcategory__all=list_subcategory)

                p= extract_basic_info( json.loads(Product.objects(**{k: v for k, v in kwargs.items() if v !=  []} ).to_json()), isAdmin)
                
                for i in p[:75]:             
                    if i["_id"]["$oid"] not in ids:
                            matching_products.append(i)
                            ids.append(i["_id"])
        if len(matching_products)<20:
            kwargs = dict(name__icontains=keyword, price__gte=price_min,price__lte=price_max, subcategory__all=list_subcategory)
            p= extract_basic_info( json.loads(Product.objects( **{k: v for k, v in kwargs.items() if v != []}).to_json()), isAdmin)
           
            for i in p[:50]:             
                if i["_id"]["$oid"] not in ids:
                        matching_products.append(i)
                        ids.append(i["_id"])
        if len(matching_products)<30:
            kwargs = dict(description__icontains=keyword, price__gte=price_min,price__lte=price_max, subcategory__all=list_subcategory)
            p= extract_basic_info( json.loads(Product.objects(**{k: v for k, v in kwargs.items() if v != []}).to_json()), isAdmin)
            
            for i in p[:25]:             
                if i["_id"]["$oid"] not in ids:
                        matching_products.append(i)
                        ids.append(i["_id"])
        if isSortByPrice:
            matching_products= sorted(matching_products, key=lambda k: k['price'],reverse=not isAscending) 
        
        
        #matching_products = extract_basic_info(json.loads(Product.objects(name__contains=keyword).to_json()))
        return Response(json_util.dumps(matching_products), mimetype="application/json", status=200)

class EmptyStockApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        out_stock = extract_basic_info(json.loads(Product.objects(stock=0).to_json()), True)
        return Response(json.dumps(out_stock), mimetype="application/json", status=200)

