from flask import Response, request
from database.models import Category
from flask_restful import Resource
from utils.utils import wrap_category_info
import json

class CategoryApi(Resource):
    def get(self):
        all_category = Category.objects()
        categories = json.loads(all_category.to_json())
        data = wrap_category_info(categories)
        return Response(json.dumps(data), mimetype="application/json", status=200)
    
