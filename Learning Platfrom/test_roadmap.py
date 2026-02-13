
import requests

def test_roadmap():
    url = "http://localhost:8001/generate/course"
    payload = {
        "topic": "Python Programming",
        "grade_level": "Beginner"
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(response.json())
        else:
            print(f"Error Status: {response.status_code}")
            print(f"Error Body: {repr(response.text)}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_roadmap()
