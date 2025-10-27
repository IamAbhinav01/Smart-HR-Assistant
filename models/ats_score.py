from parser import ResumeParser
extractor = ResumeParser()
text = extractor.text_auto_extract(r'E:\airesume\AI Scientist _ Voice, Legal, and Multimodal Intelligent Systems.pdf')
finished = extractor.enhance_with_spacy(text)
print(text,finished)


