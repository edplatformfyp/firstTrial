import requests
import json

print("\n--- Testing POST /generate/course ---")
try:
    payload = {"topic": "Quantum", "grade_level": "Grade 10"}
    response = requests.post("http://localhost:8000/generate/course", json=payload)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS! Roadmap received.")
    else:
        print(f"FAILURE: {response.text}")

except Exception as e:
    print(f"Connection failed: {e}")
