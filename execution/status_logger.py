import json
import os

STATUS_FILE = os.path.join(os.path.dirname(__file__), "..", ".tmp", "web_status.json")

def log_status(message, progress=None, status="processing"):
    """Updates the web_status.json file with current progress and message."""
    data = {"status": status, "message": message}
    
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                data = json.load(f)
        except:
            pass
            
    data["status"] = status
    data["message"] = message
    if progress is not None:
        data["progress"] = progress
        
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)
