"""
resume.py
---------
Extracts resume text and asks LLM for improvements.
"""

import pdfplumber
from llm import query_llm
from memory import load_memory, save_memory

def analyze_resume(file_path, user_id="default"):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    resume_text = text[:3000]

    prompt = f"""
Analyze this resume and give improvement suggestions:

{resume_text}
"""

    response = query_llm(prompt)

    memory = load_memory(user_id)
    memory["resume_text"] = resume_text
    memory["resume_uploaded"] = True
    save_memory(user_id, memory)

    return response
