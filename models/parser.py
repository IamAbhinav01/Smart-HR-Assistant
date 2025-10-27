from pdfminer.high_level import extract_text
import docx2txt
import os
from pyresparser import ResumeParser
import spacy

class ResumeParser:
    def __init__(self, model_name: str = "en_core_web_sm"):

        self.model_name = model_name
        self.nlp = spacy.load(model_name)

    def extract_text_from_pdf(self,pdf_path):
        return extract_text(pdf_path)

    def extract_text_from_docx(self,docx_path):
        return docx2txt.process(docx_path)

    def extract_text_from_txt(self,txt_path):
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()

    def enhance_with_spacy(self,text):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities


    def text_auto_extract(self,file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        if ext == '.docx':
            return self.extract_text_from_docx(file_path)
        if ext == '.txt':
            return self.extract_text_from_txt(file_path)

if __name__ == "__main__":
    
    parser = ResumeParser()
    text = parser.text_auto_extract(r'E:\airesume\AI Scientist _ Voice, Legal, and Multimodal Intelligent Systems.pdf')
    finished = parser.enhance_with_spacy(text)
    print(text,finished)