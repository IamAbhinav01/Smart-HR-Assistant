import json
from models.parser import AdvancedResumeParser
from models.ats_score import ResumeScorer
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

class Analyser:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0):
        self.parser = AdvancedResumeParser()
        self.score = ResumeScorer()
        
        self.model = ChatGroq(
            model=model_name,
            temperature=temperature
        )
        
        self.resume_drawbacks = PromptTemplate(
            input_variables=["result", "job_description", "score_data"],
            template="""
You are an expert ATS evaluator and HR analyst.

Use the `score_data.total` value to decide:

- If total > 70 → return positive reasons
- If total < 70 → return improvement reasons

Do NOT mention the score explicitly.
Return ONLY valid JSON:
{{
  "review": ["reason 1", "reason 2", "reason 3"]
}}

Resume: {result}
Job Description: {job_description}
Score Data: {score_data}
"""
        )

    def analyse_resume(self, file_path: str, job_description: str):
        result = self.parser.parse_resume(file_path)
        score_data = self.score.score_resume(file_path, job_description)  # Get score first

        # Create the chain
        chain = self.resume_drawbacks | self.model | JsonOutputParser()
        
        # Invoke
        try:
            response = chain.invoke({
                "result": result,
                "job_description": job_description,
                "score_data": score_data  # Pass as dict
            })
            # Validate
            if isinstance(response, dict) and "review" in response:
                return response
            else:
                return {"review": ["Analysis complete, but no specific feedback generated."]}
        except Exception as e:
            print(f"Analysis error: {e}")
            return {"review": []}

if __name__ == "__main__":
    analyser = Analyser()
    FILE_PATH = r'E:\airesume\softwareResume.pdf'
    job_text = "mlops engineer"

    print("\n=== Resume Analysis ===")
    output = analyser.analyse_resume(FILE_PATH, job_text,)
    print(output)