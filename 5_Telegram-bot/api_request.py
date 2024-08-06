import config
import requests
import os

def api_request_info_word(user_context, word):
    response = requests.get(config.BASE_API_WORD + f"wordinfo/{user_context}/{word}")
    return response.json()