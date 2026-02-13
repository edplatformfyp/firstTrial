from server.agents.planner_agent.planner import PlannerAgent
import json

print("--- Debugging Planner Agent ---")
try:
    agent = PlannerAgent()
    print("Agent initialized.")
    
    topic = "Quantum Physics"
    grade = "Grade 8"
    print(f"Requesting roadmap for: {topic} ({grade})")
    
    # We will verify the LLM response by monkey-patching or just calling it
    # But first, let's just try the normal method
    roadmap = agent.generate_roadmap(topic, grade)
    
    if roadmap:
        print("\nSUCCESS! Roadmap generated:")
        print(json.dumps(roadmap.model_dump(), indent=2))
    else:
        print("\nFAILURE: Roadmap is None.")

except Exception as e:
    print(f"\nCRASH: {e}")
    import traceback
    traceback.print_exc()
