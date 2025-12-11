from fastapi import FastAPI, UploadFile, File, Form
from models.ats_score import ResumeScorer
from models.resume_analyser import Analyser
from models.question_genrator_analyser import QuestionGenerator
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil

os.makedirs("temp_uploads", exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyser = Analyser()
scorer = ResumeScorer()
generator = QuestionGenerator()
pp.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

# Catch-all route: serve React index.html
@app.get("/{full_path:path}")
def serve_react(full_path: str):
    return FileResponse("frontend_build/index.html")
@app.post("/analyse_resume/")
async def analyse_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Generate a unique filename to prevent conflicts during parallel uploads
    unique_filename = f"{uuid.uuid4()}_{resume_file.filename}"
    temp_path = f"temp_uploads/{unique_filename}"
    
    try:
        # Save the uploaded file
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(resume_file.file, f)

        # Run analysis
        score_data = scorer.score_resume(temp_path, job_description)
        analysis = analyser.analyse_resume(temp_path, job_description)
        
        return {
            "scoreData": score_data,  # {"total": 75, "breakdown": {...}}
            "reasons": analysis.get("review", [])
        }
        
    except Exception as e:
        return {"error": str(e)}
        
    finally:
        # Clean up: Delete the temporary file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/score_resume/")
async def score_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}_{resume_file.filename}"
    temp_path = f"temp_uploads/{unique_filename}"
    
    try:
        # Save the uploaded file
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(resume_file.file, f)

        # Generate ATS score
        ats_score = scorer.score_resume(temp_path, job_description)
        
        # Handle different return formats from scorer if necessary
        # Assuming scorer returns a tuple/list where index 1 is the score
        score_val = ats_score[1] if isinstance(ats_score, (list, tuple)) else ats_score

        return {"ats_score": score_val}

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Clean up: Delete the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/practice_question/")
async def question_generate(job_description: str = Form(...)):
    try:
        questions = generator.generate_questions(job_description)
        return {"questions": questions}
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyse_answer/")
async def analyse_answer(
    question: str = Form(...),
    answer: str = Form(...)
):
    try:
        feedback = generator.analyse_answer(question, answer)
        return {"response": feedback}
    except Exception as e:
        return {"error": str(e)}
