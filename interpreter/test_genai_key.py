import sys
import traceback

# Print Python path and version info for debugging
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Trying to import google-generativeai...")

try:
    from google import genai
    print("Successfully imported google.genai")
    
    # Print API key (partially masked for security)
    api_key = "AIzaSyC2q9_9bHxvRaWPeb-ReFHNsd0czthLNHA"
    masked_key = api_key[:6] + "..." + api_key[-4:]
    print(f"Using API key: {masked_key}")
    
    # Initialize client
    client = genai.Client(api_key=api_key)
    print("Successfully initialized genai.Client")
    
    # Simple request
    print("Making API request to generate content...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello in one sentence",
    )
    
    # Print response
    print("API Response:")
    print(response.text)
    print("\nAPI key test completed successfully!")

except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Make sure google-generativeai is properly installed.")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    print("Full traceback:")
    traceback.print_exc()
