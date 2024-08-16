import json
from flask import Flask, jsonify, send_file, after_this_request
from flask_restful import Api, Resource
from llm_prompt import get_word_info, get_word_pronounce
import os

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

class WordPronounce(Resource):
    def get(self, word):
        try:
            file_path = get_word_pronounce(word)
            
            @after_this_request
            def cleanup(response): # clean the audio file after the GET request
                try:
                    os.remove(file_path)
                except Exception as e:
                    app.logger.error(f"Error deleting file: {e}")
                return response

            return send_file(file_path)
        except Exception as e:
            return {"error": "An error occurred", "details": str(e)}, 500
        
class Testing(Resource):
    def get(self):
        return "testing"

api.add_resource(Testing, "/testing")
api.add_resource(WordInfo, "/wordinfo/<string:context>/<string:word>")
api.add_resource(WordPronounce, "/wordpronounce/<string:word>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7653)