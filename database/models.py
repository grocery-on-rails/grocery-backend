from .db_init import db

# Here stores all the classes of objects
class Product(db.DynamicDocument):
    name = db.StringField(required=True)
    price = db.FloatField(required=True)
    image_list = db.ListField(db.URLField())
    subcategory = db.ListField(db.StringField())
    description = db.StringField(required=True)
    info_list = db.ListField(db.StringField())
    others = db.DynamicField()

    meta = {
        'collection': 'products'
    }

    # @queryset_manager
    # def product_lists(doc_cls, queryset):
    #     return queryset.fields(id=1, name=1, price=1, slice__image_list=1)

class Category(db.DynamicDocument):
    category = db.StringField()
    subcategory = db.ListField(db.StringField)
    meta = {
        'collection': 'meta'
    }
    
