import subprocess
import time
import sys
import os

def run_web():
    print("--- Starting LingoAcademic AI Web Dashboard ---")
    
    # 1. Start FastAPI Backend
    print("[1/2] Launching FastAPI Backend (Port 8000)...")
    backend_proc = subprocess.Popen(
        [sys.executable, "backend/main.py"],
        stdout=None,
        stderr=None,
    )
    
    # 2. Start Next.js Frontend
    print("[2/2] Launching Next.js Frontend (Port 3000)...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend",
        stdout=None,
        stderr=None,
        shell=True
    )
    
    print("\n[READY] Servers are spinning up.")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("\nKeep this terminal open. Press Ctrl+C to stop both servers.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Done.")

if __name__ == "__main__":
    run_web()
