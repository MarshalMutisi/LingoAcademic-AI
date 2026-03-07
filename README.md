# 🎓 LingoAcademic AI

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MarshalMutisi/LingoAcademic-AI)

**LingoAcademic AI** is a premium agentic pipeline designed to bridge the gap between English research and native-level German academic writing.

[**🌐 View Live Demo**](https://your-live-link.com) | [**📜 Read Documentation**](./DOCUMENTATION.md)

---

## ✨ Features

- **Agentic Academic Pipeline**: A multi-agent system that searches for real-world German sources, drafts formal text, and audits for native academic quality.
- **Robust AI Engine**: Automatic fallback between Gemini models (2.0 Flash, 1.5 Pro, etc.) and key rotation to handle quota limits seamlessly.
- **Modern Web Dashboard**: A sleek Next.js and FastAPI interface for easy interaction and real-time progress monitoring.
- **Grounding Research**: Automatically extracts and summarizes German academic frameworks to ensure credible output.
- **PDF & Text Support**: Process raw text inputs or academic PDF documents directly.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js & npm (for the web dashboard)
- A Google Gemini API Key

### 2. Setup Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_primary_key
GEMINI_API_KEY_2=your_fallback_key (optional)
```

### 3. Launch the Application

**Option A: Using Docker (Recommended)**
```bash
docker compose up --build
```

**Option B: Manual Setup**
Run the unified server script:
```powershell
python run_web.py
```
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000

---

## 🚀 Deployment

The project is designed to be easily deployed to **Render** or **Railway** using the provided `Dockerfile`. 

For step-by-step instructions on going live, see [**deployment_guide.md**](./deployment_guide.md).

## 🏗️ Architecture

The project follows a **3-Layer Architecture**:
1.  **Directive Layer**: SOPs for agents in `directives/` (Research, Writer, Critic).
2.  **Orchestration Layer**: `orchestrator.py` manages the agents' feedback loops and data flow.
3.  **Execution Layer**: Python tools in `execution/` for LLM calls, web searching, and file handling.

---

## 📂 Project Structure

- `run_web.py`: Unified launcher for the full stack.
- `orchestrator.py`: The "Brain" of the academic pipeline.
- `backend/`: FastAPI server and background processing logic.
- `frontend/`: Next.js web application.
- `directives/`: AI agent "personalities" and rules.
- `execution/`: Deterministic tools (LLM, Search, PDF).
- `.tmp/`: Intermediate drafts, research dossiers, and status logs.

---

## 📜 Documentation
For a deep dive into how the system works, the agents' logic, and the implementation history, see [DOCUMENTATION.md](./DOCUMENTATION.md).

---
<<<<<<< HEAD


=======
>>>>>>> ebbb8c0d5165e73b1a12c2a0def5cb708a0ef6cf
