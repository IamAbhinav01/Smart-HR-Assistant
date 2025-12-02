from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

class QuestionGenerator:
    def __init__(self, model_name="moonshotai/kimi-k2-instruct-0905", temperature=0):

        # Initialize LLM properly
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature
        )

        # Question generator prompt
        
        self.question_generator = PromptTemplate(
    input_variables=['job_description'],
    template="""
You are an HR interviewer. Based on the job description below, generate exactly 3 HR interview questions.

❗IMPORTANT: Return the output strictly in the following JSON format:

[
  {{ "q": "Question 1 here" }},
  {{ "q": "Question 2 here" }},
  {{ "q": "Question 3 here" }}
]

Do NOT add any explanations or text outside the JSON.

Job Description:
{job_description}
"""
)
        self.question_analyser = PromptTemplate(
    input_variables=['question', 'answer'],
    template="""
You are an HR answer evaluator. Analyse the candidate's answer for correctness, relevance, clarity, and completeness.

Your task:
- Evaluate the given answer.
- Provide 3 short pieces of feedback:
    1. What was good.
    2. What is missing.
    3. What to improve.
- Output ONLY in the array format below.

❗STRICT OUTPUT FORMAT (no extra text):

[
  {{ "a": "Feedback point 1" }},
  {{ "a": "Feedback point 2" }},
  {{ "a": "Feedback point 3" }}
]

Question:
{question}

Candidate Answer:
{answer}
"""
)


    # -------------------
    # Generate Questions
    # -------------------
    def generate_questions(self, job_description: str):
        chain = self.question_generator | self.llm | JsonOutputParser()
        return chain.invoke({"job_description": job_description})

    # -------------------
    # Analyse Answer
    # -------------------
    def analyse_answer(self, question: str, answer: str):
        chain = self.question_analyser | self.llm | JsonOutputParser()
        return chain.invoke({"question": question, "answer": answer})


# ---------------------------
# RUN THE CLASS
# ---------------------------
if __name__ == "__main__":
    generator = QuestionGenerator()

    job_text = "mlops engineer"
    print("\n=== Questions ===")
    questions = generator.generate_questions(job_text)
    print(questions)

    print("\n=== Sample Answer Evaluation ===")
    feedback = generator.analyse_answer(
        "What is MLOps?",
        "MLOps is deploying machine learning models in production."
    )
    print(feedback)
