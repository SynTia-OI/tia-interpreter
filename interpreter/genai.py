from google import genai

client = genai.Client(api_key="AIzaSyC2q9_9bHxvRaWPeb-ReFHNsd0czthLNHA")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)