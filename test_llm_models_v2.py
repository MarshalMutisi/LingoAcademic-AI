import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-8b"
]

with open("model_test_results_v2.txt", "w") as f:
    f.write("--- Testing Model Availability ---\n")
    for m_name in models_to_test:
        try:
            f.write(f"Testing {m_name}...\n")
            model = genai.GenerativeModel(m_name)
            response = model.generate_content("Hi", generation_config={"max_output_tokens": 5})
            f.write(f"SUCCESS: {m_name} worked.\n")
        except Exception as e:
            f.write(f"FAILED: {m_name} - {str(e)}\n")
        f.flush()
        time.sleep(1)
