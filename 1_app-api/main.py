import json
import requests
import os
from flask import Flask, jsonify, send_file, after_this_request, send_from_directory
from flask_restful import Api, Resource
from llm_prompt import get_word_info, get_word_pronounce

app = Flask(__name__)
api = Api(app)

#TODO only allow GET methods
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


class WordPronounce(Resource):
    def get(self, word):
        try:
            filepath = get_word_pronounce(word)
            if filepath is None or not os.path.exists(filepath):
                print("[ERROR] Audio file was not created.")
                return {"error": "Audio file was not created"}, 500

            print(f"[INFO] Audio file created at {filepath}")
            return send_file(filepath)
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            return {"error": "An error occurred", "details": str(e)}, 500


class Testing(Resource):
    def get(self):
        return "testing"

api.add_resource(Testing, "/testing")
api.add_resource(WordInfo, "/wordinfo/<string:context>/<string:word>")
api.add_resource(WordPronounce, "/wordpronounce/<string:word>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7653)