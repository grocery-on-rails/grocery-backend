from flask import Flask
from flask import jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_restful import Api
from resources.routes import initialize_routes
from database.db_init import initialize_db
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'MONGODB_DB': 'grocery',
    'MONGODB_HOST': os.getenv('MONGODB_URI')
}

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not Found'}), 404)
# app.register_blueprint()

print(os.getenv('MONGODB_URI'))

api = Api(app)
#bcrypt = Bcrypt(app)

initialize_db(app)
initialize_routes(api)

if(__name__ == "__main__"):
    app.run(debug=True)