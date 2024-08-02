import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "wordinfo/Network-engineering-and-cybersecurity/passion")
print(response.json())
