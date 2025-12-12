# Smart HR Assistant (Smart-HR-Assistant)

AI-powered Resume Analysis & ATS Score Evaluation Tool

Smart HR Assistant is a full-stack web application that helps job seekers analyze their resumes against a target job description. It provides structured insights and an ATS (Applicant Tracking System) score using a FastAPI backend and a React frontend.

## Table of contents

- [Features](#features)
- [Project structure](#project-structure)
- [Architecture overview](#architecture-overview)
- [Backend (FastAPI)](#backend-fastapi)
  - [Endpoints](#endpoints)
  - [Running locally (backend)](#running-locally-backend)
- [Frontend (React)](#frontend-react)
  - [Running locally (frontend)](#running-locally-frontend)
- [API examples](#api-examples)
- [Security & production notes](#security--production-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Next steps / TODOs](#next-steps--todos)

## Features

- Resume analysis: extract skills, keywords and assess content match to a job description.
- ATS scoring: compute an ATS-style score and highlight missing keywords.
- Simple, API-driven frontend for upload and results display.

## Project structure

Top-level layout (important files):

```
Smart-HR-Assistant/
├── main.py                # FastAPI backend entry point
├── models/                # Resume analysis and scoring logic
│   ├── resume_analyser.py
│   ├── ats_score.py
│   └── parser.py
├── temp_uploads/          # Temporarily stored resume files (created at runtime)
├── requirements.txt       # Python backend dependencies
└── src/                   # React frontend
    ├── pages/
    │   ├── home.js       # Resume upload + job description
    │   └── Analysis.js    # Displays analysis results
    ├── components/
    │   └── FileUploader.js
    ├── App.js
    └── package.json
```

## Architecture overview

1. User uploads a PDF resume and supplies a job description on the frontend.
2. Frontend sends two POST requests to the backend:
   - `/analyse_resume/` → returns structured analysis JSON.
   - `/score_resume/` → returns ATS score.
3. Frontend navigates to the Analysis page and displays results returned by the backend.

## Backend (FastAPI)

Location: `main.py`

### Endpoints

- `POST /analyse_resume/`

  - Form fields: `resume_file` (file), `job_description` (string).
  - Action: saves the uploaded PDF into `temp_uploads/` and calls `models.resume_analyser.Analyser.analyse_resume()`.
  - Response: JSON `{ "analysis": <object> }`.

- `POST /score_resume/`
  - Form fields: same as `/analyse_resume/`.
  - Action: saves file and calls `models.ats_score.ResumeScorer.score_resume()`.
  - Response: JSON `{ "ats_score": <number> }`.

### Running locally (backend)

PowerShell example:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000/`.

## Frontend (React)

Location: `src/`

### Running locally (frontend)

PowerShell example:

```powershell
npm install
npm start
```

The frontend is typically available at `http://localhost:3000/`.

### Notes about integration

- The frontend posts multipart/form-data to `http://localhost:8000/analyse_resume/` and `/score_resume/` (see `src/pages/home.js`).
- If backend is hosted elsewhere, update the URLs or move them to configuration.
- Configure CORS in FastAPI when serving frontend from a different origin.

## API examples

PowerShell curl examples:

```powershell
curl -X POST "http://localhost:8000/analyse_resume/" -F "resume_file=@C:\path\to\resume.pdf" -F "job_description=Data Scientist"

curl -X POST "http://localhost:8000/score_resume/" -F "resume_file=@C:\path\to\resume.pdf" -F "job_description=Data Scientist"
```

## Security & production notes

- Sanitize or generate server-side unique filenames (UUID) instead of trusting user-supplied names.
- Implement CORS, authentication, rate-limiting, and request size limits before public deployment.
- Use HTTPS in production. Prefer ephemeral storage for uploads and implement automatic cleanup.
- If analysis is slow or resource-heavy, run it in background workers and serve progress via polling or WebSockets.

## Troubleshooting

- "Failed to contact the analysis service": verify the FastAPI server is running and accessible at the configured URL (default `http://localhost:8000/`).
- 500 server errors: check the uvicorn console for tracebacks and ensure Python dependencies and model files are present.
- File size: frontend blocks >5 MB by default; adjust client and server limits if needed.

## Contributing

1. Fork the repository and create a branch.
2. Add tests and documentation updates where relevant.
3. Open a pull request with a clear description of changes.

## Next steps / TODOs

- Move API base URL to an environment/config variable in the frontend.
- Add server-side filename sanitization and cleanup for `temp_uploads/`.
- Improve UX for long-running analysis (progress indicator, background jobs).
- Add unit and integration tests for `models/` and API endpoints.
