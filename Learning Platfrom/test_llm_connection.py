
from server.core.llm import LLMService

def test():
    print("Testing LLMService...")
    llm = LLMService()
    print(f"Provider: {llm.provider}")
    print(f"Groq Client: {llm.groq_client}")
    
    response = llm.generate("Say hello", "You are a helpful assistant.")
    print(f"Response: {response}")

if __name__ == "__main__":
    test()
