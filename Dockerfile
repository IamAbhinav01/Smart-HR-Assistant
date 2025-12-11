# ==========================================
# STAGE 1: React Frontend Build
# ==========================================
FROM node:20-slim AS react-builder

# Set working directory
WORKDIR /app/frontend

# Copy package files first for caching
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps --prefer-offline --no-audit

# Copy source code
COPY src/ ./src
COPY public/ ./public

# Debug: list pages directory (optional, helps troubleshoot missing files)
RUN echo "=== Frontend src/pages ===" && ls -la src/pages/

# Build React frontend
RUN npm run build

# Verify build success
RUN if [ ! -d "build" ]; then echo "❌ Frontend build failed"; exit 1; fi

# ==========================================
# STAGE 2: FastAPI Backend
# ==========================================
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=10000 \
    TEMP_UPLOAD_DIR=/app/temp_uploads

WORKDIR /app

# Copy Python requirements
COPY requirements.txt ./

# Install system deps & Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY main.py ./ 
COPY models/ ./models/
COPY README.md ./ || true
COPY .env.example ./ || true

# Copy React build from frontend stage
COPY --from=react-builder /app/frontend/build ./frontend_build

# Verify frontend build copied
RUN if [ -d "frontend_build" ]; then echo "✅ Frontend build copied"; else echo "⚠️ frontend_build missing"; fi

# Create temp_uploads directory
RUN mkdir -p /app/temp_uploads && chmod 755 /app/temp_uploads && echo "✅ Created temp_uploads"

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose backend port
EXPOSE 10000

# Optional healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:10000/').read()" || exit 1

# Startup command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
