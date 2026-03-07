# 🚀 LingoAcademic AI — Deployment Guide

This guide walks you through getting LingoAcademic AI live on the internet using **Render** (free tier, easiest for resumes) or **Railway**. Both platforms support Docker-based deployments.

---

## Prerequisites

- [ ] Push your project to a **public GitHub repository**
- [ ] Make sure `.env` is in `.gitignore` (it already is ✅)
- [ ] Have your `GEMINI_API_KEY` ready

---

## Option A: Deploy on Render (Recommended)

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "feat: add Docker, rate limiting, and BYOK support"
git push origin main
```

### Step 2 — Create Two Services on Render

Go to [render.com](https://render.com) → **New** → **Web Service** → Connect your GitHub repo.

#### Service 1: Python Backend (FastAPI)

| Setting | Value |
|---|---|
| **Name** | `lingoAcademic-backend` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `python backend/main.py` |
| **Port** | `8000` |

**Environment Variables:**
```
GEMINI_API_KEY = your-gemini-api-key-here
```

#### Service 2: Next.js Frontend

| Setting | Value |
|---|---|
| **Name** | `lingoAcademic-frontend` |
| **Root Directory** | `frontend` |
| **Runtime** | `Node` |
| **Build Command** | `npm ci && npm run build` |
| **Start Command** | `npm start` |
| **Port** | `3000` |

**Environment Variables:**
```
NEXT_PUBLIC_API_URL = https://lingoAcademic-backend.onrender.com
```

> ⚠️ Replace the URL above with the actual URL Render gives your backend service.

---

## Option B: Deploy on Railway (One-Click, Easier)

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub Repo**
2. Railway will auto-detect the `Dockerfile` and build it
3. Add environment variables in the **Variables** tab:
   - `GEMINI_API_KEY` = your key
4. Railway will give you a public URL automatically

---

## Option C: Test Locally with Docker First

```bash
# Build and run (from the project root)
docker compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## 🔐 API Key Security Summary

| Layer | Status |
|---|---|
| `.env` in `.gitignore` | ✅ Safe — never committed to git |
| Key set as Render/Railway env var | ✅ Safe — encrypted, never exposed to users |
| Optional user BYOK key | ✅ Sent server-side only, never stored |
| Rate limiter (5 req/min per IP) | ✅ Active — protects against abuse |

---

## 🎓 Resume Tip

On your resume/portfolio, list the live URL and link to the GitHub repo. You can write:

> *LingoAcademic AI — Full-stack AI pipeline (FastAPI + Next.js) that transforms English research prompts into German academic text using a 3-agent Gemini pipeline. Deployed on Render with Docker, rate limiting, and BYOK API key support.*
