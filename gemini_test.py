
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found!")
    raise SystemExit

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Say hello! My AI Vision Detector is ready."
    )

    print("Gemini Response:")
    print(response.text)

except Exception as error:
    print("Gemini Error:", error)
