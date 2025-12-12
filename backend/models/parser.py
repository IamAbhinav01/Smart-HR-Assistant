from pdfminer.high_level import extract_text
import docx2txt
import os
import spacy
from dotenv import load_dotenv
from typing import List, Tuple


from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


load_dotenv()



def _extract_text_from_pdf_func(pdf_path: str) -> str:
    """The raw function to extract text content from a PDF file."""
    return extract_text(pdf_path)

def _extract_text_from_docx_func(docx_path: str) -> str:
    """The raw function to extract text content from a DOCX file."""
    return docx2txt.process(docx_path)

def _extract_text_from_txt_func(txt_path: str) -> str:
    """The raw function to extract text content from a TXT file."""
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

def _enhance_with_spacy_func(text: str, model_name: str = "en_core_web_sm") -> List[Tuple[str, str]]:
    """The raw function to analyze text using spaCy to extract Named Entities."""
    nlp = spacy.load(model_name)
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities



@tool
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text content from a PDF file. 
    Call this tool only if the LLM is explicitly asked to handle a PDF file path.
    """
    return _extract_text_from_pdf_func(pdf_path)

@tool
def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts text content from a DOCX file. 
    Call this tool only if the LLM is explicitly asked to handle a DOCX file path.
    """
    return _extract_text_from_docx_func(docx_path)

@tool
def extract_text_from_txt(txt_path: str) -> str:
    """
    Extracts text content from a TXT file. 
    Call this tool only if the LLM is explicitly asked to handle a TXT file path.
    """
    return _extract_text_from_txt_func(txt_path)

@tool
def enhance_with_spacy(text: str) -> List[Tuple[str, str]]:
    """
    Analyzes the provided resume text chunk to extract Named Entities 
    (e.g., PERSON, ORG, DATE, GPE) to aid in structured parsing.
    """
   
    return _enhance_with_spacy_func(text)


ALL_TOOLS = [
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    enhance_with_spacy
]



class AdvancedResumeParser:
    def __init__(self, model_name: str = "moonshotai/kimi-k2-instruct-0905"):
        self.llm = ChatGroq(
            temperature=0, 
            model_name=model_name
        )

    def parse_resume(self, file_path: str):
        # 1. Extract the text yourself (no tool calling)
        resume_text = self.text_auto_extract(file_path)

        # 2. Ask the LLM directly (no tools allowed)
        prompt = f"""
        You are a resume parser for ATS.
        Parse the following resume text into:
        - Name
        - Contact
        - Summary
        - Experience
        - Education
        - Skills
        
        Resume:
        {resume_text}
        """

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def text_auto_extract(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[-1].lower()
        
        if ext == '.pdf':
            return _extract_text_from_pdf_func(file_path)
        if ext == '.docx':
            return _extract_text_from_docx_func(file_path)
        if ext == '.txt':
            return _extract_text_from_txt_func(file_path)

        raise ValueError(f"Unsupported file type: {ext}")