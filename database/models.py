from enum import unique
from mongoengine.queryset.manager import queryset_manager
from .db_init import db
from flask_bcrypt import generate_password_hash, check_password_hash

# Here stores all the classes of objects
class Product(db.DynamicDocument):
    name = db.StringField(required=True)
    price = db.FloatField(required=True)
    image_list = db.ListField(db.URLField())
    subcategory = db.ListField(db.StringField())
    description = db.StringField(required=True)
    others = db.DynamicField()
    scraped_url = db.URLField()
    stock = db.IntField(required=True)
    discount = db.FloatField()
    meta = {
        'collection': 'products'
    }

class Category(db.Document):
    category = db.StringField(required=True, unique=True)
    subcategory = db.ListField(db.StringField())
    meta = {
        'collection': 'meta'
    }

class User(db.DynamicDocument):
    username = db.StringField()
    password = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    privilege = db.BooleanField(default=False)
    cart = db.ListField(db.DictField(), null=True)
    address = db.ListField(db.StringField())
    orders = db.ListField(db.DictField())
    recently_viewed = db.ListField(db.StringField())
    meta = {
        'collection': 'users'
    }
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
