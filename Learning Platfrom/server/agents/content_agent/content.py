import json
from server.core.llm import LLMService
from server.shared.schemas import Chapter, ChapterContent, QuizQuestion
from typing import Optional

class ContentAgent:
    def __init__(self):
        self.llm = LLMService()

    def generate_chapter_content(self, chapter: Chapter) -> Optional[ChapterContent]:
        system_prompt = (
            "You are an expert world-class educator. Write a COMPREHENSIVE, DEEP STYLED lecture "
            "for the provided chapter. The content must be at least 1000 words long. "
            "Structure it with: 1. Introduction, 2. Core Concepts (detailed), 3. Real-world Examples, "
            "4. Interactive scenarios/Thought Experiments, 5. Summary. "
            "Also generate a challenging 5-question quiz. "
            "Return ONLY valid JSON. IMPORTANT: The 'content_markdown' field must be a SINGLE line string with all newlines escaped as \\n. "
            "Do not put raw newlines inside the JSON string values. "
            "For Math/Equations: Always use LaTeX. Use '$' for inline math (e.g., $E=mc^2$) and '$$' for block math. "
            "Format: { \"chapter_title\": String, \"content_markdown\": String, "
            "\"quiz\": [{ \"question\": String, \"options\": [String], \"correct_answer\": Int }] }"
        )
        user_prompt = f"Write content for Chapter {chapter.chapter_number}: {chapter.title}. Description: {chapter.description}"
        
        response_text = self.llm.generate(user_prompt, system_prompt, json_mode=True)
        
        if not response_text:
            return None

        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(cleaned_text)
            return ChapterContent(**data)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON content: {cleaned_text}")
            return None
        except Exception as e:
            print(f"Validation error: {e}")
            return None
