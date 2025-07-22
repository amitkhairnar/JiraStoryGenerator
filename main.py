# ==============================================================================
# File: main.py
# Component: 1. Input Interface (FastAPI) - UPDATED
# ==============================================================================
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestration_service import process_new_story_request
import os

app = FastAPI(
    title="AI Jira Story Generator (Offline)",
    description="Takes a one-liner prompt and creates a detailed story in a local file.",
    version="1.3.0"
)

# Enable CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    message: str
    output_file: str

@app.post("/create-story/", response_model=StoryResponse)
async def create_story_endpoint(request: StoryRequest):
    """
    This endpoint receives the one-liner prompt and orchestrates the
    creation of a detailed story.
    """
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    try:
        # Trigger the orchestration service
        output_file = process_new_story_request(request.prompt)
        
        return StoryResponse(
            message="Story file created successfully!",
            output_file=output_file
        )
    except Exception as e:
        print(f"An error occurred in the workflow: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serves the main HTML user interface.
    """
    html_file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(html_file_path):
        with open(html_file_path, "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="<h1>Interface not found</h1>", status_code=404)
