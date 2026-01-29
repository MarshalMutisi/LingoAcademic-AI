from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import json
from pydantic import BaseModel

# Add root to path so we can import orchestrator and utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator import run_pipeline as run_orchestrator

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATUS_FILE = os.path.join(os.path.dirname(__file__), "..", ".tmp", "web_status.json")

class ProcessRequest(BaseModel):
    text: str
    max_iterations: int = 2

@app.get("/")
def read_root():
    return {"message": "LingoAcademic AI Backend is running"}

@app.get("/status")
def get_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {"status": "idle"}

def update_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def background_process(text: str, max_iterations: int):
    try:
        update_status({"status": "processing", "message": "Starting pipeline...", "progress": 10})
        
        # Run the existing pipeline
        # For now, we reuse the existing file-based orchestrator
        # We'll save the input to input.txt first
        input_path = os.path.join(os.path.dirname(__file__), "..", "input_web.txt")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        run_orchestrator(input_path, max_iterations=max_iterations)
        
        # Read the final output to send back
        final_output_path = os.path.join(os.path.dirname(__file__), "..", "final_academic_output.md")
        final_text = ""
        if os.path.exists(final_output_path):
            with open(final_output_path, "r", encoding="utf-8") as f:
                final_text = f.read()
                
        update_status({
            "status": "completed", 
            "message": "Pipeline finished!", 
            "result": final_text,
            "progress": 100
        })
    except Exception as e:
        print(f"ERROR IN BACKGROUND PROCESS: {str(e)}")
        update_status({
            "status": "error", 
            "message": f"Pipeline failed: {str(e)}", 
            "progress": 0
        })

@app.post("/process")
def process_text(request: ProcessRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_process, request.text, request.max_iterations)
    return {"status": "started", "message": "Research and writing analysis initiated."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
