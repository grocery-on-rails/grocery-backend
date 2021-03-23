from .db_init import db

# Here stores all the classes of objects
class Meat(db.DynamicDocument):
    name = db.StringField(required=True)
    price = db.FloatField(required=True)
    unit = db.StringField(required=True)
    quantity = db.StringField()
    category = db.StringField(required=True)
    subcategory = db.ListField()
    country = db.StringField()
    image_list = db.ListField(db.URLField())
    desc = db.ListField(db.StringField())
    info_list = db.ListField(db.StringField())
    scrapped_url = db.URLField()

    meta = {
        'collection': 'meat'
    }

class Vegetable(db.DynamicDocument):
    name = db.StringField()
    price = db.FloatField()
    unit = db.StringField()
    quantity = db.StringField()
    category = db.StringField()
    subcategory = db.ListField()
    country = db.StringField()
    image_list = db.ListField(db.URLField())
    desc = db.ListField(db.StringField())
    info_list = db.ListField(db.StringField())
    scrapped_url = db.URLField()
    meta = {
        'collection': 'vegetables'
    }
    
