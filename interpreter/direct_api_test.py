import requests
import json
import sys

print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")

API_KEY = "AIzaSyC2q9_9bHxvRaWPeb-ReFHNsd0czthLNHA"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

# Test with a simple prompt
prompt = "Say hello in one sentence."

# Construct the request payload
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

# Add API key as a query parameter
url = f"{GEMINI_API_URL}?key={API_KEY}"

try:
    print(f"Making API request to Google Gemini API...")
    response = requests.post(url, json=payload)
    
    # Check response status
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("API key is valid and working correctly!")
        result = response.json()
        
        # Extract and print the response text
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]
            if "parts" in content and len(content["parts"]) > 0:
                text = content["parts"][0]["text"]
                print(f"\nAPI Response: {text}")
        else:
            print("Unexpected response format:")
            print(json.dumps(result, indent=2))
    else:
        print(f"API Error: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 400:
            print("API key might be invalid or malformed.")
        elif response.status_code == 401:
            print("API key is invalid or unauthorized.")
        elif response.status_code == 403:
            print("API key doesn't have permission to access this model or resource.")
        elif response.status_code == 429:
            print("Rate limit exceeded or quota exhausted.")
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
