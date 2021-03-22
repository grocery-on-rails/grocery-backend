from flask import Flask
from flask import jsonify, make_response

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if(__name__ == "__main__"):
    app.run(debug=True)