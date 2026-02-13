import os
import sys
print(f"DEBUG: sys.stdout.encoding = {sys.stdout.encoding}")
import time
from typing import Optional
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai

load_dotenv()

class LLMService:
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        with open("debug_init.txt", "a") as f:
             f.write(f"Init LLMService. Provider: {provider}\n")
             f.write(f"GROQ_KEY: {'Found' if self.groq_api_key else 'Missing'}\n")
             f.write(f"CWD: {os.getcwd()}\n")

        self.groq_client = None
        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"Failed to init Groq client: {e}")

        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Failed to init Gemini client: {e}")

    def generate(self, prompt: str, system_instruction: str = "", retries: int = 3, json_mode: bool = False) -> Optional[str]:
        # Try primary provider first
        try:
            if self.provider == "groq" and self.groq_client:
                return self._call_groq(prompt, system_instruction, json_mode)
            elif self.provider == "gemini" and self.gemini_api_key:
                return self._call_gemini(prompt, system_instruction)
        except Exception as e:
             error_msg = f"Primary provider ({self.provider}) failed: {e}"
             print(error_msg)
             with open("debug_log.txt", "a") as f:
                 f.write(error_msg + "\n")
 
        # Fallback logic could go here, but for now we just return None or retry internally
        return None

    def _call_groq(self, prompt: str, system_instruction: str, json_mode: bool = False) -> str:
        try:
            kwargs = {
                "messages": [
                    {
                        "role": "system",
                        "content": system_instruction,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "model": "llama-3.1-8b-instant",
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            chat_completion = self.groq_client.chat.completions.create(**kwargs)
            
            if hasattr(chat_completion, 'usage'):
                usage = chat_completion.usage
                print("DEBUG: ABOUT TO PRINT TOKEN USAGE")
                print(f"Token Usage: {usage.total_tokens} (In: {usage.prompt_tokens}, Out: {usage.completion_tokens})")
                
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_msg = f"Groq SDK Error: {e}"
            print(error_msg)
            with open("debug_log.txt", "a") as f:
                f.write(error_msg + "\n")
            raise e

    def _call_gemini(self, prompt: str, system_instruction: str) -> str:
        try:
            full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
             print(f"Gemini SDK Error: {e}")
             raise e
