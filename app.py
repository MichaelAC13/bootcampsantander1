from flask import Flask 
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__) 
cors = CORS(app, resources={r"/": {"origins": "*.*"}})

@app.route("/", methods=['GET']) 
@cross_origin()
def home(): 
    return jsonify({
        "api": "API",
        "description":"Extract, transform, load",
        "version": "1.0.0"
    })
    
@app.route("/orders", methods=['POST']) 
@cross_origin()
def orders(): 
    payload = request.get_json()
    return request

    
if __name__ == '__main__':
    app.run(debug=True, port=5000)