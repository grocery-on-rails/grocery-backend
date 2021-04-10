from flask import Flask
from flask import jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_restful import Api
from resources.routes import initialize_routes
from database.db_init import initialize_db
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGODB_HOST'] = os.getenv('MONGODB_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)

if(__name__ == "__main__"):
  app.run(debug=True)
