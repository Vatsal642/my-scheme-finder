import requests
import json
import time

URL = "http://127.0.0.1:8000/query"

test_queries = [
    "I am a 28 year old woman farmer from UP, income below 1.5 lakh",
    "I am a 15 year old girl student from Gujarat, family income 50,000",
    "I am a 65 year old widow from Karnataka with no income",
    "I am an unemployed 22 year old engineering graduate from Delhi",
    "I am a 45 year old male farmer from Maharashtra, income 2 lakh"
]

for i, q in enumerate(test_queries):
    print(f"\\n--- Test {i+1} ---")
    print(f"Query: {q}")
    start_time = time.time()
    try:
        response = requests.post(URL, json={"query": q, "filters": {}}, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Answer:\\n", data.get("answer"))
            print("\\nSources:", data.get("sources"))
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Request failed: {e}")
    print(f"Time taken: {time.time() - start_time:.2f}s")
