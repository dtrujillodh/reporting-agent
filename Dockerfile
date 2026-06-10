# Stage 1: Build the React frontend
FROM node:22-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Python backend and copy frontend assets
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy backend and agent code
COPY backend/ ./backend/
COPY agent/ ./agent/

# Copy the build output from the frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# Set environment variables
ENV PORT=8001
EXPOSE 8001

# Start the application
CMD ["uv", "run", "python", "backend/main.py"]
