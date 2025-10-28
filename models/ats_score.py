from parser import AdvancedResumeParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq


class ResumeScorer:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0.8):
 
        self.parser = AdvancedResumeParser()

  
        self.model = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_retries=2
        )

    
        self.resume_score_prompt = PromptTemplate(
            input_variables=["result", "job_description"],
            template="""
Act as a HR Manager with 20 years of experience.
You are already given a resume data from a resume which has been parsed,
Compare the resume data provided below with the job description given below.
Check for key skills in the resume data that are related to the job description.
Rate the resume data out of 100 based on the matching skill set.
Assess the score with high accuracy.

Resume: {result}
Job Description: {job_description}
I want the response ONLY as in json format for api format so that i can send in front end :
score:<number>
"""
        )

        self.chain = self.resume_score_prompt | self.model

    def score_resume(self, resume_path: str, job_description: str):
      
        raw_text = self.parser.text_auto_extract(resume_path)

        llm_output = self.parser.llm_tool_call(raw_text)
        parsed_result = llm_output.content

        
        result = self.chain.invoke({
            "result": parsed_result,
            "job_description": job_description
        })

        return result.content  


class RoleMatching:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0.8):
        self.parser = AdvancedResumeParser()

        self.model = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_retries=2
        )

        self.role_matching_prompt = PromptTemplate(
            input_variables=["result"],
            template="""
Act as a professional Career Role Analyzer.
Analyze the resume and suggest the roles the candidate is most suitable for.

Return ONLY JSON in the format:
{{
  "suggested_roles": ["role1", "role2", "role3", ...]
}}

Resume:
{result}
"""
        )

        self.chain = self.role_matching_prompt | self.model

    def get_roles(self, resume_path: str):
        raw_text = self.parser.text_auto_extract(resume_path)
        llm_output = self.parser.llm_tool_call(raw_text)
        parsed_result = llm_output.content

        result = self.chain.invoke({"result": parsed_result})
        return result.content


if __name__ == "__main__":
    scorer = ResumeScorer()
    matcher = RoleMatching()

    FILE_PATH = r'E:\airesume\myResume.docx'
    job_text = "mlops engineer"

    print("\n=== Resume Score ===")
    output = scorer.score_resume(FILE_PATH, job_text)
    print(output)

    print("\n=== Suggested Roles ===")
    output2 = matcher.get_roles(FILE_PATH)
    print(output2)