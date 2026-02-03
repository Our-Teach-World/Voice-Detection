import requests
import base64
import json
import time
import subprocess
import os

def test_api():
    # 1. Start the server
    server_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "API_KEY": "sk_test_123456789"}
    )
    
    retries = 5
    while retries > 0:
        try:
            requests.get("http://127.0.0.1:8000/docs")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            retries -= 1
    
    if retries == 0:
        print("Server did not start in time.")
        server_process.terminate()
        return

    try:
        # 2. Prepare request
        with open("english.mp3", "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
            
        payload = {
            "language": "English",
            "audioFormat": "mp3",
            "audioBase64": audio_b64
        }
        headers = {
            "x-api-key": "sk_test_123456789",
            "Content-Type": "application/json"
        }
        
        # 3. Send request
        print("Sending request to API...")
        response = requests.post("http://127.0.0.1:8000/api/voice-detection", json=payload, headers=headers)
        
        # 4. Print results
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        
    finally:
        server_process.terminate()

if __name__ == "__main__":
    test_api()
