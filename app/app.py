from flask import Flask
from flask import jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_restful import Api
from resources.routes import initialize_routes
import json

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
 'host': 'mongodb://localhost/grocery'
}

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not Found'}), 404)
# app.register_blueprint()

api = Api(app)
bcrypt = Bcrypt(app)


initialize_routes(api)

if(__name__ == "__main__"):
    app.run(debug=True)