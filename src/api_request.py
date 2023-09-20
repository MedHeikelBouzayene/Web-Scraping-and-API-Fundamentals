import requests
import json

base_url = "https://itunes.apple.com/search"

params = {
    "term": "samara",
    "country": "TN",
    "limit": 200
}

response = requests.get(base_url, params=params)

print(response.json()["resultCount"])