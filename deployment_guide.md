# 🚀 LingoAcademic AI — Single Link Deployment Guide

This guide gets your project live on **Render** with **one single URL** (Monolith setup). This is the most efficient way to host a live demo on a resume.

---

## 1. Push Your Project to GitHub

Make sure all your local changes are pushed to your repository:
```powershell
git add .
git commit -m "🚀 Unified monolith build for single-link live demo"
git push origin main
```

---

## 2. Deploy on Render (Free Tier)

### Step 1: Create a Web Service
- Go to [render.com](https://render.com)
- Click **New +** → **Web Service**
- Connect your GitHub repository: `MarshalMutisi/LingoAcademic-AI`

### Step 2: Configure the Service
Render will automatically detect your `Dockerfile`. Use these settings:

| Setting | Value |
|---|---|
| **Name** | `lingo-academic` |
| **Runtime** | `Docker` |
| **Instance Type** | `Free` |

### Step 3: Add Environment Variables
Click the **Environment** tab and add your key:
- `GEMINI_API_KEY` = `your-actual-api-key-here`

### Step 4: Deploy
Click **Create Web Service**. 

---

## 3. Verify Your Live Demo

1.  Wait about 2-5 minutes for Render to finish the build.
2.  Once it says "Live", click the URL Render gives you (e.g., `https://lingo-academic.onrender.com`).
3.  **Your website should load immediately.**
4.  Test it: Enter text, click generate, and enjoy your one-link live demo!

---

## 🔐 Why this is better for your resume:
- **One URL**: Recruiters don't have to visit multiple links.
- **Microservice Build**: You used a "Multi-stage Docker build" (look at your `Dockerfile`). This shows you know high-end Devops.
- **Resource Efficient**: Only uses one Render slot.
