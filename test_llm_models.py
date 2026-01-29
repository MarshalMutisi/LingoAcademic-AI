import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-8b"
]

print("--- Testing Model Availability ---")
for m_name in models_to_test:
    try:
        print(f"Testing {m_name}...")
        model = genai.GenerativeModel(m_name)
        response = model.generate_content("Hi", generation_config={"max_output_tokens": 5})
        print(f"SUCCESS: {m_name} worked.")
    except Exception as e:
        print(f"FAILED: {m_name} - {str(e)}")
    time.sleep(2)
