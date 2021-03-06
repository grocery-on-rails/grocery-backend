from flask import Response, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from mongoengine.errors import DoesNotExist, ValidationError
from database.models import Product, User
from flask_restful import Resource
from utils.utils import *
from urllib.parse import unquote
from bson import json_util, objectid
import json


# Method for handling API requests related to an item
class ItemsApi(Resource):
    @jwt_required(optional=True)
    def get(self):
        all_products = Product.objects()
        recently_viewed = extract_basic_info(json.loads(all_products[0:5].to_json()))
        new_arrivals = extract_basic_info(json.loads(all_products[5:10].to_json()))
        today_deals = extract_basic_info(json.loads(Product.objects(discount__gt=0)[:20].to_json()))
        pipeline=[{"$unwind": "$orders" },{"$unwind": "$orders.cart" },{"$group":{"_id":"$orders.cart.product_id", "quantity":{"$sum": "$orders.cart.quantity"}}}, {"$sort":{"quantity":-1}}]
        sales=[json.loads(Product.objects(id=i["_id"])[0].to_json()) for i in list(User.objects.aggregate(pipeline))[:10]]
        
        top_sells = extract_basic_info(sales)
        fresh_vegies = extract_basic_info(json.loads(Product.objects()[0:16].to_json()))
        data = {}
        data['slides'] = list(["https://via.placeholder.com/150", "https://via.placeholder.com/100", "https://via.placeholder.com/200"])
        data['content'] = list([{'title': 'Today\'s Deals', 'content': today_deals}, \
        {'title': 'New Arrivals', 'content': new_arrivals}, {'title': 'Top Sellers', 'content': top_sells}, \
        {'title': 'Veggies', 'content': fresh_vegies}])
        if get_jwt_identity():
            # print([i for i in User.objects(id=get_jwt_identity())[0].recently_viewed])
            recently_viewed=extract_basic_info(([json.loads(Product.objects(id=i)[0].to_json()) for i in User.objects(id=get_jwt_identity())[0].recently_viewed[:-11:-1]]))
            
            data['content'].append({'title': 'Recently Viewed', 'content': recently_viewed})
            recently_viewed=User.objects(id=get_jwt_identity())[0].recently_viewed
            # recently_viewed= map(objectid.ObjectId,recently_viewed)
            recently_viewed=[objectid.ObjectId(i) for i in recently_viewed]
            pipeline=[

                    {"$match":{"_id":{"$in":recently_viewed}}},
                    {"$project": {"_id":0,"subcategory":1}},

            
            ]
            s=[]
            for i in list(Product.objects().aggregate(pipeline)):
                    s=s+i["subcategory"]
            s=list(set(s))
            pipeline=[

                    {"$match":{"subcategory":{"$in":s}}},
                    {"$sample": {"size":20}},

            
            ]
            
            data['content'].append({'title': 'Recommended Products', 'content': extract_basic_info((list(Product.objects().aggregate(pipeline))))[:100]})
        return Response(json_util.dumps(data), mimetype="application/json", status=200)

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
    @jwt_required(optional=True)
    def get(self, id):
        try:
            item = Product.objects().get(id=id).to_json()
        except DoesNotExist:
            return {'error': 'Product ID not found'}, 404
        else:
             
            if get_jwt_identity():
                user_id=get_jwt_identity()
                if User.objects(id=user_id,recently_viewed=id):
                    User.objects(id=user_id).update_one(pull__recently_viewed=id)
                User.objects(id=user_id).update_one(push__recently_viewed=id)
                # print(User.objects(id=user_id)[0].recently_viewed)
            
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
                if (body.get(field) != None):
                    item[field] = body.get(field)
            item.save()
            return {'msg': 'Success'}, 200

class ItemSearchApi(Resource):
    @jwt_required(optional=True)
    def post(self, raw_keyword):
        user_id = get_jwt_identity()
        isAdmin = False
        if user_id:
            user = User.objects.get(id=user_id)
            if user.privilege:
                isAdmin = True

        body = request.get_json()

        isSortByPrice = False
        isAscending = False
        
        match={"$match":{}}
        price_min  = 0
        price_max = 999999
        list_subcategory = []
        if body:    
            if body.get('sort') == 'price+':
                isSortByPrice = True
                isAscending = True
            elif body.get('sort') == 'price-':
                isSortByPrice = True
            else:
                pass
            
            if body.get('price_min'):
                price_min = int(body.get('price_min'))
                match["$match"]["price"]={"$gte":price_min}
            if body.get('price_max'):
                price_max = int(body.get('price_max'))
                match["$match"]["price"]={"$lte":price_max}
            
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

class CategorySearchApi(Resource):
    def post(self):
        body = request.get_json()
        isSortByPrice = False
        isAscending = False
        if body:    
            if body.get('sort') == 'price+':
                isSortByPrice = True
                isAscending = True
            elif body.get('sort') == 'price-':
                isSortByPrice = True
            if body.get('subcategory'):
                subcat = body.get('subcategory')
                if isSortByPrice:
                    if isAscending:
                        subcat_product = extract_basic_info(json.loads(Product.objects(subcategory=subcat).order_by('+price').to_json()))
                    else:
                        subcat_product = extract_basic_info(json.loads(Product.objects(subcategory=subcat).order_by('-price').to_json()))
                else:
                    subcat_product = extract_basic_info(json.loads(Product.objects(subcategory=subcat).to_json()))
                return Response(json_util.dumps(subcat_product), mimetype="json/application", status=200)
        return {'error': 'Subcategory not found/given'}, 401

class EmptyStockApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        if not user.privilege:
            return {'error': 'Elevated privilege required'}, 403
        out_stock = extract_basic_info(json.loads(Product.objects(stock=0).to_json()), True)
        return Response(json.dumps(out_stock), mimetype="application/json", status=200)

