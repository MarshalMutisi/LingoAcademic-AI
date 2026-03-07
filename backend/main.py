from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import json
import time
from collections import defaultdict
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# Static files path (Next.js export)
FRONTEND_OUT = os.path.join(os.path.dirname(__file__), "..", "frontend", "out")
STATUS_FILE = os.path.join(os.path.dirname(__file__), "..", ".tmp", "web_status.json")

# ---------------------------------------------------------------------------
# Rate Limiter: max 5 requests per IP per minute
# ---------------------------------------------------------------------------
RATE_LIMIT = 5        # max requests
RATE_WINDOW = 60      # seconds
_rate_store: dict = defaultdict(list)  # ip -> [timestamps]

def check_rate_limit(ip: str):
    now = time.time()
    timestamps = _rate_store[ip]
    # Drop timestamps older than the window
    _rate_store[ip] = [t for t in timestamps if now - t < RATE_WINDOW]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT} requests per minute."
        )
    _rate_store[ip].append(now)

# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------
class ProcessRequest(BaseModel):
    text: str
    max_iterations: int = 2
    api_key: str = ""  # Optional: user's own Gemini API key


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
# @app.get("/")
# def read_root():
#     return {"message": "LingoAcademic AI Backend is running"}


@app.get("/status")
def get_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {"status": "idle"}


def update_status(data):
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)


def background_process(text: str, max_iterations: int, user_api_key: str):
    try:
        update_status({"status": "processing", "message": "Starting pipeline...", "progress": 10})

        # If user provided their own key, use it; otherwise fall back to env var
        if user_api_key:
            os.environ["GEMINI_API_KEY_OVERRIDE"] = user_api_key
        else:
            os.environ.pop("GEMINI_API_KEY_OVERRIDE", None)

        # Save the input text for the orchestrator
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
    finally:
        # Always clean up the override so it doesn't bleed into subsequent requests
        os.environ.pop("GEMINI_API_KEY_OVERRIDE", None)


@app.post("/process")
async def process_text(request: ProcessRequest, req: Request, background_tasks: BackgroundTasks):
    # Rate limit by client IP
    client_ip = req.client.host if req.client else "unknown"
    check_rate_limit(client_ip)

    background_tasks.add_task(
        background_process,
        request.text,
        request.max_iterations,
        request.api_key,
    )
    return {"status": "started", "message": "Research and writing analysis initiated."}


# Serve Frontend Static Files
if os.path.exists(FRONTEND_OUT):
    # Mount the 'out' directory for static files (html, css, js)
    app.mount("/", StaticFiles(directory=FRONTEND_OUT, html=True), name="frontend")
    
    # Catch-all route to serve index.html for client-side routing
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: Exception):
        # Only reroute to index.html if the request is not for the API
        if not request.url.path.startswith("/status") and not request.url.path.startswith("/process"):
            return FileResponse(os.path.join(FRONTEND_OUT, "index.html"))
        return JSONResponse(status_code=404, content={"detail": "Not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
