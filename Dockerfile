# ================================
# STAGE 1 — TAILWIND CSS BUILD
# ================================
FROM node:20-slim AS tailwind-builder

WORKDIR /app

# Copy Tailwind + config
COPY tailwind.config.js package*.json ./
COPY static ./static
COPY templates ./templates

RUN npm install -D tailwindcss

# Build Tailwind output.css
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify



# ================================
# STAGE 2 — REACT BUILD (CRA)
# ================================
FROM node:20-slim AS react-builder

WORKDIR /app/frontend

COPY src ./src
COPY public ./public
COPY package*.json ./

RUN npm install
RUN npm run build



# ================================
# STAGE 3 — FASTAPI BACKEND
# ================================
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy Tailwind output.css
COPY --from=tailwind-builder /app/static/css/output.css ./static/css/output.css

# Copy React build into a folder for FastAPI
COPY --from=react-builder /app/frontend/build ./frontend_build

# Expose Render port
ENV PORT=10000
EXPOSE 10000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
