from llm_prompt import get_word_info_json

from flask import Flask, request, jsonify
app = Flask(__name__)


# That's why the "Click here to download" prompts the window AND download, the automatic request
@app.route("/") # default route
def home():
    return "Home"



# @app.route('/', methods=['GET']) #TODO confirm
# def

result = get_word_info_json()
print(result)

if __name__ == "__main__":
    app.run(debug=True)