from parser import AdvancedResumeParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

class Analyser:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0.8):
        self.parser = AdvancedResumeParser()

        self.model  = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_retries=2
        )
        self.resume_drawbacks = PromptTemplate(
            input_variables=["result","job_descripion"],
            template="""
            You are an expert ATS reviewer and HR analyst.
Your task is to analyze the given resume against the provided job description and find any drawbacks, missing skills, experience gaps, or mismatches.

Return the response **only** in valid JSON format suitable for API usage.
Do not include any extra commentary or text outside JSON.

Resume: {result}

Job Description: {job_description}

Expected JSON format:
{{
  "review": "<detailed but concise feedback on drawbacks and areas of improvement in the resume with respect to the job description>"
}}
"""
        )
        self.chain = self.resume_drawbacks | self.model

    def analyse_resume(self, resume_path: str, job_description: str):
        raw_text = self.parser.text_auto_extract(resume_path)

        llm_output = self.parser.llm_tool_call(raw_text)
        parsed_result = llm_output.content

        
        result = self.chain.invoke({
            "result": parsed_result,
            "job_description": job_description
        })

        return result.content

if __name__ == "__main__":
    analyser = Analyser()
    FILE_PATH = r'E:\airesume\myResume.docx'
    job_text = "mlops engineer"

    print("\n=== Resume Analysis ===")
    output = analyser.analyse_resume(FILE_PATH, job_text)
    print(output)