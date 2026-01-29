import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from execution.status_logger import log_status

load_dotenv()

# FALLBACK MODEL LIST
FALLBACK_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash"]

print(f"\n[BOOT] LLM_UTILS LOADED - FALLBACK_MODELS: {FALLBACK_MODELS}")

def call_llm(prompt, system_prompt="You are a helpful assistant.", model=None):
    """
    Standard interface for LLM calls using Google Gemini with automatic model fallback and key rotation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    api_key_2 = os.getenv("GEMINI_API_KEY_2")
    keys = [k for k in [api_key, api_key_2] if k]

    if not keys:
        return "Error: No GEMINI_API_KEY found in .env"

    models_to_try = [model] if model else FALLBACK_MODELS

    for target_model in models_to_try:
        log_status(f"Trying Gemini model: {target_model}...")
        
        for i, key in enumerate(keys):
            try:
                genai.configure(api_key=key)
                print(f"\n>>> [AI ENGINE V6] Model: {target_model} | Key: {i+1}")
                
                model_instance = genai.GenerativeModel(
                    model_name=target_model,
                    system_instruction=system_prompt
                )
                
                # Add a tiny throttle to help with stability
                time.sleep(1)
                
                response = model_instance.generate_content(prompt)
                if response.text:
                    return response.text
                return "Error: Empty response."
                
            except Exception as e:
                err = str(e)
                print(f"[ENGINE ERROR] {target_model} (Key {i+1}) failed: {err}")
                
                # If it's a quota error, we either try the next key or the next model
                if "429" in err:
                    if i < len(keys) - 1:
                        log_status(f"Quota exceeded for {target_model}. Rotating to next key...", status="warning")
                        continue
                    else:
                        log_status(f"Quota exhausted for {target_model} on all keys. Falling back to next model...", status="warning")
                        break # Try next model
                
                # For other errors (except transient ones), we might want to return immediately or try next model
                log_status(f"Error with {target_model}: {err[:50]}...", status="warning")
                break # Try next model
    
    return "Error: All models and keys failed or reached quota."
