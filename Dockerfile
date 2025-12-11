# ================================
# STAGE 1 — REACT BUILD (CRA + Tailwind)
# ================================
# STAGE 1 — REACT BUILD (CRA + Tailwind)
# ================================
FROM node:20-slim AS react-builder

WORKDIR /app/frontend

# Copy package.json and package-lock.json first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source and public folders
COPY src/ ./src
COPY public/ ./public

# Optional: debug files
RUN ls -R src/pages

# Build React
RUN npm run build


# ================================
# STAGE 2 — FASTAPI BACKEND
# ================================
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install backend dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy React build from frontend stage
COPY --from=react-builder /app/frontend/build ./frontend_build

# Expose port for Render
ENV PORT=10000
EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
