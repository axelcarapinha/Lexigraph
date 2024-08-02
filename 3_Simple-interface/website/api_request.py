import config
import requests

#TODO change for the specific role
def api_request_info_word(user, word):
    response = requests.get(config.BASE_API_WORD + "wordinfo/Network-engineering-and-cybersecurity/passion")
    return response.json()