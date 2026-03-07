# syntax=docker/dockerfile:1

# ============================================================
# Stage 1: Build the Next.js frontend
# ============================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Install dependencies first (better layer caching)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build


# ============================================================
# Stage 2: Python backend + serve frontend via Next.js
# ============================================================
FROM python:3.11-slim AS final

WORKDIR /app

# Install Node.js (needed to run `next start` in production)
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy all project files
COPY . .

# Bring in the built Next.js app from the previous stage
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules

# Create the .tmp directory the app writes to at runtime
RUN mkdir -p .tmp

# Expose ports
EXPOSE 8000 3000

# Launch both services with run_web.py
CMD ["python", "run_web.py"]
