import json
from models.parser import AdvancedResumeParser
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

class ResumeScorer:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0):
        self.parser = AdvancedResumeParser()
        self.model = ChatGroq(model=model_name, temperature=temperature)

        self.resume_score_prompt = PromptTemplate(
            input_variables=["result", "job_description"],
            template="""
Act as an experienced HR Manager and ATS evaluator.
Compare the resume with the job description and score it out of 100.

Return ONLY valid JSON in the following format:
{{
  "total": <number>,
  "breakdown": {{
    "Content": <number>,
    "Structure": <number>,
    "ATS": <number>,
    "Tailoring": <number>
  }}
}}

Resume: {result}
Job Description: {job_description}
"""
        )

    def score_resume(self, file_path: str, job_description: str):
        result = self.parser.parse_resume(file_path)  # Your parsing logic here
        
        # Create the chain: Prompt -> Model -> JSON Parser
        chain = self.resume_score_prompt | self.model | JsonOutputParser()
        
        # Invoke the chain
        try:
            response = chain.invoke({"result": result, "job_description": job_description})
            # Validate it's a dict with expected keys
            if isinstance(response, dict) and "total" in response:
                return response
            else:
                # Fallback if parsing fails
                return {"total": 50, "breakdown": {"Content": 50, "Structure": 50, "ATS": 50, "Tailoring": 50}}
        except Exception as e:
            print(f"Scoring error: {e}")
            return {"total": 0, "breakdown": {"Content": 0, "Structure": 0, "ATS": 0, "Tailoring": 0}}

if __name__ == "__main__":
    scorer = ResumeScorer()
   

    FILE_PATH = r'E:\airesume\myResume.docx'
    job_text = "mlops engineer"

    print("\n=== Resume Score ===")
    parsed, score  = scorer.score_resume(FILE_PATH, job_text)
    print("ATS SCORE =", score)

  
