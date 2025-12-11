# =====================================================================
# STAGE 1: React Frontend Build
# =====================================================================
# Build the React (Create React App) frontend with TailwindCSS
# Uses Node 20 slim for a smaller base image and faster builds
FROM node:20-slim AS react-builder

# Set working directory for frontend build
WORKDIR /app/frontend

# Copy package manifests (locked first to leverage layer caching)
COPY package*.json ./

# Install npm dependencies with clean install
# --legacy-peer-deps ensures compatibility with all packages
RUN npm ci --prefer-offline --no-audit

# Copy frontend source code
# Using specific directories to avoid copying unnecessary files
COPY src/ ./src
COPY public/ ./public

# Debug: list files in pages directory to verify structure
# This helps troubleshoot missing files during build
RUN echo "=== Frontend files structure ===" && \
    ls -la src/pages/ && \
    echo "=== Public assets ===" && \
    ls -la public/

# Build the React production bundle
# Tailwind CSS will be processed during this build step
# Output goes to ./build/ directory
RUN npm run build

# Verify build was successful
RUN if [ ! -d "build" ]; then echo "❌ Build failed: 'build' directory not found"; exit 1; fi && \
    echo "✅ Frontend build successful"


# =====================================================================
# STAGE 2: Python FastAPI Backend (Final Image)
# =====================================================================
# This stage runs the backend API and serves the frontend static files
# Uses Python 3.10 slim for a lightweight production image
FROM python:3.10-slim

# Set environment variables for optimal Python behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# ═══════════════════════════════════════════════════════════════════
# Install system dependencies and Python packages
# ═══════════════════════════════════════════════════════════════════

# Copy Python requirements first (layer caching optimization)
COPY requirements.txt ./

# Install Python dependencies
# Using --no-cache-dir to keep image size minimal
# Remove apt cache after installation to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ═══════════════════════════════════════════════════════════════════
# Copy application code
# ═══════════════════════════════════════════════════════════════════

# Copy backend source code
# Important: This includes main.py, models/, and other backend files
COPY main.py ./
COPY models/ ./models/

# Copy all other necessary files (config, readme, etc.)
# Excluding items in .dockerignore if present
COPY README.md ./ || true
COPY .env.example ./ || true

# ═══════════════════════════════════════════════════════════════════
# Copy React frontend build from Stage 1
# ═══════════════════════════════════════════════════════════════════

# Copy the built React app into backend's static serving directory
# FastAPI (via Starlette) can serve these static files
COPY --from=react-builder /app/frontend/build ./frontend_build

# Verify frontend files were copied
RUN echo "=== Verifying frontend build copy ===" && \
    if [ -d "frontend_build" ]; then \
        echo "✅ Frontend build copied successfully" && \
        ls -la frontend_build/ | head -20; \
    else \
        echo "⚠️  Warning: frontend_build directory not found"; \
    fi

# ═══════════════════════════════════════════════════════════════════
# Create runtime directories with proper permissions
# ═══════════════════════════════════════════════════════════════════

# Create temp_uploads directory for resume file storage
# Use -p to avoid errors if directory exists
RUN mkdir -p /app/temp_uploads && \
    chmod 755 /app/temp_uploads && \
    echo "✅ Created temp_uploads directory"

# Create a non-root user for security (optional but recommended)
# This reduces the blast radius if the container is compromised
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# ═══════════════════════════════════════════════════════════════════
# Expose and configure runtime
# ═══════════════════════════════════════════════════════════════════

# Backend API port
EXPOSE 10000

# Environment variables for runtime
# These can be overridden when running the container
ENV PORT=10000 \
    TEMP_UPLOAD_DIR=/app/temp_uploads

# ═══════════════════════════════════════════════════════════════════
# Health check (optional but recommended for orchestration)
# ═══════════════════════════════════════════════════════════════════

# Verify the API is responding every 30 seconds
# Timeout after 10 seconds, fail after 3 failed checks
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:10000/').read()" || exit 1

# ═══════════════════════════════════════════════════════════════════
# Startup command
# ═══════════════════════════════════════════════════════════════════

# Run FastAPI with Uvicorn
# --host 0.0.0.0: Listen on all network interfaces (required for containers)
# --port: Bound to PORT env var
# --reload: Disabled in production; can be toggled via ENV
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
