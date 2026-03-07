# syntax=docker/dockerfile:1

# ============================================================
# Stage 1: Build the Next.js frontend (Static Export)
# ============================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Install dependencies first
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy source and build static export
COPY frontend/ ./
RUN npm run build


# ============================================================
# Stage 2: Final Production Image (Python Backend)
# ============================================================
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy all project files
COPY . .

# Bring in the built static frontend files from Stage 1
# This goes into frontend/out so backend/main.py can serve it
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Ensure the .tmp directory exists for status files
RUN mkdir -p .tmp

# Expose only the backend port
EXPOSE 8000

# Start the monolith app (FastAPI will serve the frontend)
CMD ["python", "backend/main.py"]
