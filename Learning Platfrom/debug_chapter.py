from server.agents.content_agent.content import ContentAgent
from server.shared.schemas import Chapter
import json

print("--- Debugging Content Agent ---")
try:
    agent = ContentAgent()
    print("Agent initialized.")
    
    # Mock a chapter object
    chapter = Chapter(
        chapter_number=1,
        title="Introduction to Quantum Physics",
        description="Basic principles of quantum mechanics."
    )
    
    print(f"Requesting detailed content for: {chapter.title}")
    
    # Call the agent
    content = agent.generate_chapter_content(chapter)
    
    if content:
        print("\nSUCCESS! Content generated:")
        print(f"Title: {content.chapter_title}")
        print(f"Content Length: {len(content.content_markdown)} chars")
        print("Quiz Questions:", len(content.quiz))
    else:
        print("\nFAILURE: Content is None.")

except Exception as e:
    print(f"\nCRASH: {e}")
    import traceback
    traceback.print_exc()
