from server.core.llm import LLMService
import os

print("--- Starting Groq Verification ---")
try:
    llm = LLMService(provider="groq")
    print(f"API Key Loaded: {'Yes' if llm.groq_api_key else 'No'}")
    if llm.groq_api_key:
        print(f"API Key prefix: {llm.groq_api_key[:5]}...")
    
    print("Attempting to generate text...")
    response = llm.generate("Hello", "You are a test bot.")
    
    if response:
        print("SUCCESS! Response received:")
        print(response)
    else:
        print("FAILURE: No response received (None returned).")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
