# LingoAcademic AI: Project Documentation

## 1. Overview
**LingoAcademic AI** is an advanced agentic pipeline designed to transform English source material into high-quality, research-grounded German academic text. It uses a **3-Layer Architecture** to ensure reliability, combining agentic reasoning with deterministic execution.

## 2. Core Architecture
The project follows a modular design pattern that separates concerns into three distinct layers:

### Layer 1: Directive (The Mind)
Located in `directives/`, these are **Standard Operating Procedures (SOPs)** written in Markdown. They define the "personalities" and rules for our AI agents:
*   **Librarian (`research_agent.md`)**: Extracts concepts and searches for German academic sources.
*   **Writer (`writer_agent.md`)**: Drafts formal German academic text (*Wissenschaftliches Arbeiten*).
*   **Critic (`critic_agent.md`)**: Audits the draft against native university standards.

### Layer 2: Orchestration (The Brain)
The **`orchestrator.py`** manages the flow of information between agents. It:
1.  Loads the input (Text or PDF).
2.  Initializes the **Librarian** to research grounding material.
3.  Runs a **Feedback Loop** (default 2 iterations) where the **Writer** drafts and the **Critic** provides feedback until approval or maximum iterations are reached.

### Layer 3: Execution (The Tools)
Located in `execution/`, these are deterministic Python scripts that perform the actual work:
*   **`llm_utils.py`**: Handles calls to Gemini with robust fallback and key rotation logic.
*   **`search_utils.py`**: Performs web searches for academic grounding.
*   **`file_utils.py`**: Manages PDF extraction and file saving.
*   **`status_logger.py`**: Provides real-time progress updates to the Web UI.

---

## 3. The pipeline Process
The system operates in a sequential pipeline:

1.  **Ingestion**: User uploads a PDF or enters text via the Web Dashboard.
2.  **Librarian Phase**: The Librarian extracts key academic concepts and generates a search query. It then performs a search to find German frameworks and literature.
3.  **Grounding**: The results are compiled into a "Research Grounding Dossier" to ensure the AI doesn't hallucinate definitions.
4.  **Drafting (Writer)**: The Writer takes the English source + Research Dossier and produces a German draft using formal academic style (*Nominalstil*, passive voice).
5.  **Audit (Critic)**: The Critic professor reviews the draft for "German professor" standards.
6.  **Loop**: If the Critic requires revisions, the feedback goes back to the Writer for a second pass.
7.  **Output**: The final APPROVED version is saved as `final_academic_output.md`.

---

## 4. How it was Built (Steps of Implementation)

### Step 1: Core Tooling & PDF Extraction
We started by building the `execution/` layer. We implemented PDF text extraction and search integration so the AI had "eyes" onto the real world.

### Step 2: The 3-Agent SOP System
We defined the specific rules for the librarian, writer, and critic. This was crucial to ensure the output didn't sound like a "Google Translation" but like a native German academic paper.

### Step 3: Orchestrator Development
We built the logic to connect these agents. We implemented the file-based memory system in `.tmp/` so the system can "remember" drafts and feedback across iterations.

### Step 4: Web Integration (Full Stack)
We built a modern web dashboard:
*   **Backend**: A FastAPI server that runs the pipeline in the background.
*   **Frontend**: A Next.js application that provides a premium user interface with progress bars and real-time status updates.

### Step 5: Robust AI Engine (Reliability)
The final step (and recent fix) was building the **Engine V6** in `llm_utils.py`. This ensures the project stays alive even when hitting API limits by automatically falling back to different Gemini models and rotating API keys.

---

## 5. Summary of Files
*   `run_web.py`: The entry point. Launches both Backend and Frontend.
*   `orchestrator.py`: The master logic of the academic pipeline.
*   `backend/main.py`: The API bridge.
*   `frontend/`: The Next.js dashboard code.
*   `.tmp/`: Where all intermediate drafts and research are stored.
*   `final_academic_output.md`: Your final result!
