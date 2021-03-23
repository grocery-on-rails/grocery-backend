from .db_init import db

# Here stores all the classes of objects
class Meat(db.Document):
    def __init__(self):
        self.item_name = db.StringField(required=True, unique=True)
        self.price = db.FloatField(required=True)
        self.unit = db.StringField(required=True)
        self.quantity = db.StringField(required=True)
        self.category = db.StringField(required=True)
        self.subcategory = db.ListField()
        self.country = db.StringField()
        self.image_url = db.URLField(required=True)
        self.desc = db.ListField(db.StringField())
        self.info_list = db.ListField(db.StringField())
        self.scrapped_url = db.URLField()

class Vegetable(db.Document):
    def __init__(self):
        self.item_name = db.StringField(required=True, unique=True)
        self.price = db.FloatField(required=True)
        self.unit = db.StringField(required=True)
        self.quantity = db.StringField(required=True)
        self.category = db.StringField(required=True)
        self.subcategory = db.ListField()
        self.country = db.StringField()
        self.image_url = db.URLField(required=True)
        self.desc = db.ListField(db.StringField())
        self.info_list = db.ListField(db.StringField())
        self.scrapped_url = db.URLField()

