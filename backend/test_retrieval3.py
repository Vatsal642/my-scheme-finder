import requests
import json

URL = "http://127.0.0.1:8000/query"

q = "I am a 28 year old woman farmer from Uttar Pradesh, income below 1.5 lakh"
response = requests.post(URL, json={"query": q, "filters": {}}, timeout=30)
print(response.json()["answer"])
