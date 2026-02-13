from server.core.llm import LLMService

print("Testing LLM Service...")
try:
    llm = LLMService(provider="groq")
    print(f"Provider: {llm.provider}")
    print(f"Key present: {bool(llm.groq_api_key)}")
    
    response = llm.generate("Hello, say hi!", "You are a helpful assistant.")
    print(f"Response: {response}")

except Exception as e:
    print(f"CRASH: {e}")
