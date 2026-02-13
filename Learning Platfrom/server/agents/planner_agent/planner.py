import json
from server.core.llm import LLMService
from server.shared.schemas import CourseRoadmap, Chapter
from typing import Optional

class PlannerAgent:
    def __init__(self):
        self.llm = LLMService()

    def generate_roadmap(self, topic: str, grade_level: str) -> Optional[CourseRoadmap]:
        system_prompt = (
            "You are an expert curriculum planner. Create a structured learning roadmap "
            "for the given topic and grade level. Return ONLY valid JSON matching the following structure: "
            "{ \"topic\":String, \"chapters\": [{ \"chapter_number\": Int, \"title\": String, \"description\": String }] }"
        )
        user_prompt = f"Create a course roadmap for '{topic}' at a '{grade_level}' level."
        
        with open("debug_planner.txt", "a", encoding="utf-8") as f:
            f.write(f"DEBUG: Generating roadmap for {topic}\n")
        
        response_text = self.llm.generate(user_prompt, system_prompt, json_mode=True)
        
        with open("debug_planner.txt", "a", encoding="utf-8") as f:
            f.write(f"DEBUG: Roadmap response: {response_text}\n")
        
        if not response_text:
            return None

        # Clean markdown code blocks if present
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(cleaned_text)
            # Validate with Pydantic
            roadmap = CourseRoadmap(**data)
            return roadmap
        except json.JSONDecodeError:
            msg = f"Failed to parse JSON: {cleaned_text}"
            print(msg)
            with open("debug_planner.txt", "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            return None
        except Exception as e:
            msg = f"Validation error: {e}"
            print(msg)
            with open("debug_planner.txt", "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            return None
