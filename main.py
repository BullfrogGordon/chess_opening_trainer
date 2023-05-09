from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from pymongo import MongoClient
import random

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

openings_post_args = reqparse.RequestParser()
openings_post_args.add_argument("fen", location='json', type=str, help="Opening Moves", required=True)
openings_post_args.add_argument("name", location='json', type=str, help="Opening Name", required=True)

client = MongoClient('mongodb://localhost:27017/')
db = client['chess'] 
collection = db['openings']

def get_random_opening():
    count = collection.count_documents({})
    random_index = random.randint(0, count-1)
    random_doc = collection.find().limit(1).skip(random_index)[0]
    return random_doc

class Opening(Resource):
    def get(self):
        opening = get_random_opening()
        opening_name = {
            "name": opening['name']
            }
        
        return opening_name
    
    def post(self):
        args = openings_post_args.parse_args()
        fen = args['fen']
        name = args['name']
        opening_doc = collection.find_one({"name": name})
        if opening_doc and opening_doc["fen"] == fen:
            response = {"response": "Good job!"}
            return response, 201
        else:
            response = {"response": "Nope! Try again!"}
            return response, 201
    
api.add_resource(Opening, "/openingquiz")

if __name__ == "__main__":
    app.run(debug=True)