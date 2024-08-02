from flask import Flask, jsonify
from flask_restful import Api, Resource
from llm_prompt import get_word_info
import json

app = Flask(__name__)
api = Api(app)

class WordInfo(Resource):
    def get(self, context, word):
        try:
            json_string = get_word_info(context, word)
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            return {"error": "Invalid JSON data", "details": str(e)}, 400
        except Exception as e: # general errors (other than JSON)
            return {"error": "An error occurred", "details": str(e)}, 500
        
        return jsonify(data)

api.add_resource(WordInfo, "/wordinfo/<string:context>/<string:word>") # proper route

if __name__ == "__main__":
    app.run(debug=True, port=5001)