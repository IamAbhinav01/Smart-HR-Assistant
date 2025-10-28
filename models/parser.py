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
        
        self.llm = ChatGroq(temperature=0, model_name=model_name)
        
        self.available_tools = ALL_TOOLS
       
        self.tool_map = {tool.name: tool for tool in ALL_TOOLS}

    def text_auto_extract(self, file_path: str) -> str:
        """Determines file type and uses the appropriate raw function for text extraction."""
        ext = os.path.splitext(file_path)[-1].lower()
        
        if ext == '.pdf':
            return _extract_text_from_pdf_func(file_path) 
        if ext == '.docx':
            return _extract_text_from_docx_func(file_path)
        if ext == '.txt':
            return _extract_text_from_txt_func(file_path)
            
        raise ValueError(f"Unsupported file type: {ext}")

    def llm_tool_call(self, resume_text: str):
        """
        Initializes an agent-like chain to parse the resume text using the LLM and its tools.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an **extreme-level, highly-achievable resume parser** for an ATS. Your task is to analyze the provided resume text in minute detail and output the parsed data using rich markdown formatting. You have access to tools; if you need to perform entity recognition, call the `enhance_with_spacy` tool with the resume text. The final output MUST be a comprehensive markdown document suitable for ATS validation, including Name, Contact, Summary, Experience, Education, and Skills."),
            ("user", 
             "Resume to parse: \n\n{resume}\n\nStrictly follow the markdown output format for ATS.")
        ])
        
       
        llm_with_tools = self.llm.bind_tools(self.available_tools)
        
        chain = prompt | llm_with_tools
        response = chain.invoke({"resume": resume_text})
        
        
        if response.tool_calls:
            print(f"--- LLM requested {len(response.tool_calls)} tool call(s) ---")
            tool_messages = []
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                print(f"Executing tool: {tool_name} with args: {tool_args}")
                
                
                tool_output = self.tool_map[tool_name].invoke(tool_args)
                
              
                tool_messages.append(ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_id,
                ))

           
            print("--- Feeding tool results back to LLM for final response ---")
            
            
            final_messages = prompt.format_messages(resume=resume_text) + [response] + tool_messages
            
            final_response = self.llm.invoke(final_messages)
            return final_response
            
        return response



if __name__ == "__main__":
    # NOTE: ADJUST THIS PATH TO YOUR ACTUAL FILE LOCATION
    FILE_PATH = r'E:\airesume\myResume.docx'
    
    if not os.path.exists(FILE_PATH):
        print(f"ERROR: File not found at path: {FILE_PATH}")
    else:
        parser = AdvancedResumeParser()
        
        try:
            # 1. Extract raw text using the direct, callable function
            raw_text = parser.text_auto_extract(FILE_PATH)
            print("--- Extracted Raw Text (First 300 chars) ---")
            print(raw_text[:300] + "...")
            
            # 2. Call the LLM/Agent for parsing (including tool use if requested)
            llm_output = parser.llm_tool_call(raw_text)
            
            print("\n--- Final LLM Parsed Output (ATS Ready) ---")
            print(llm_output.content)

        except ValueError as e:
            print(f"Error during file processing: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")