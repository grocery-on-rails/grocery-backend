from flask_mongoengine import MongoEngine
import os

# Initialize the database here

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)