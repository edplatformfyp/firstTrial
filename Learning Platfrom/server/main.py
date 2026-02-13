from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from server.shared.schemas import CourseRequest, CourseRoadmap, ChapterContent, ChapterRequest
from server.agents.planner_agent.planner import PlannerAgent
from server.agents.content_agent.content import ContentAgent
# from server.agents.proctor_agent.proctor import ProctorAgent
import asyncio

app = FastAPI(title="EduCore API", version="1.0.0")

from fastapi.staticfiles import StaticFiles
from server.agents.media_agent.media import MediaAgent
import os
from pydantic import BaseModel

app.mount("/static", StaticFiles(directory="client/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    error_msg = f"Unhandled Exception: {exc}"
    print(error_msg)
    with open("debug_error.txt", "a") as f:
        f.write(error_msg + "\n")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "debug": str(exc)},
    )

planner_agent = PlannerAgent()
content_agent = ContentAgent()
media_agent = MediaAgent()

@app.get("/")
def read_root():
    return {"message": "EduCore API is running"}

@app.post("/generate/course")
async def generate_course(request: CourseRequest):
    """
    Orchestrates the course generation:
    1. Plan roadmap (Planner Agent)
    2. Generate first chapter content (Content Agent)
    """
    print(f"Generating course for: {request.topic} ({request.grade_level})")
    with open("debug_main.txt", "a") as f:
        f.write(f"Received request: {request.topic}, {request.grade_level}\n")
    
    # Step 1: Generate Roadmap
    roadmap = planner_agent.generate_roadmap(request.topic, request.grade_level)
    print("DEBUG: Roadmap generated object")
    with open("debug_main.txt", "a") as f:
        f.write("Roadmap generated object. Returning...\n")
        
    if not roadmap:
        raise HTTPException(status_code=500, detail="Failed to generate roadmap")
    
    # Step 2: Return Roadmap immediately (Frontend will request chapters later)
    return {
        "roadmap": roadmap,
        "first_chapter_content": None, # Deprecated in favor of on-demand
        "message": "Roadmap generated successfully."
    }

@app.post("/generate/chapter")
async def generate_chapter(request: ChapterRequest):
    print(f"Generating content for Chapter {request.chapter.chapter_number}: {request.chapter.title}")
    content = content_agent.generate_chapter_content(request.chapter)
    
    if not content:
        raise HTTPException(status_code=500, detail="Failed to generate chapter content")
        
    return content

class VideoRequest(BaseModel):
    topic: str
    content_markdown: str

@app.post("/generate/video")
async def generate_video(request: VideoRequest):
    print(f"Generating video for: {request.topic}")
    video_path = await media_agent.generate_video(request.topic, request.content_markdown)
    
    if not video_path:
        raise HTTPException(status_code=500, detail="Failed to generate video")
        
    return {"video_url": video_path}

@app.websocket("/ws/proctor/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    # try:
    #     while True:
    #         # Expecting bytes (frame)
    #         data = await websocket.receive_bytes()
            
    #         # Process frame
    #         status = proctor_agent.process_frame(data, user_id)
            
    #         # Send back status
    #         await websocket.send_json(status.model_dump())
            
    # except WebSocketDisconnect:
    #     print(f"User {user_id} disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8001, reload=True)
