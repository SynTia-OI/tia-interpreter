import sys

# Write output to a file for better visibility
with open('test_output.txt', 'w') as f:
    f.write(f"Python Version: {sys.version}\n")
    f.write(f"Python Executable: {sys.executable}\n\n")
    
    # Try to import requests
    f.write("Testing imports:\n")
    try:
        import requests
        f.write("✓ requests module is available\n")
        
        # Test direct API call with minimal code
        api_key = "AIzaSyC2q9_9bHxvRaWPeb-ReFHNsd0czthLNHA"
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": "Hello"}]}]
        }
        
        f.write("Making API request...\n")
        response = requests.post(url, json=payload)
        f.write(f"Response Status: {response.status_code}\n")
        
        if response.status_code == 200:
            f.write("API KEY IS VALID AND WORKING\n")
            f.write(f"Response: {response.text[:100]}...\n")
        else:
            f.write("API KEY IS NOT WORKING\n")
            f.write(f"Error: {response.text}\n")
            
    except ImportError:
        f.write("✗ requests module is NOT available\n")
    except Exception as e:
        f.write(f"Error making request: {type(e).__name__}: {str(e)}\n")
    
    # Try to import google and google.genai
    try:
        import google
        f.write("✓ google module is available\n")
        try:
            import google.genai
            f.write("✓ google.genai module is available\n")
        except ImportError:
            f.write("✗ google.genai module is NOT available\n")
    except ImportError:
        f.write("✗ google module is NOT available\n")

print("Test completed. Results written to test_output.txt")
