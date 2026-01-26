"""
llm.py
------
Central LLM wrapper using Gemini.

KEY IDEA:
- We do NOT block questions in code
- We instruct the LLM about its scope
- LLM politely refuses off-topic questions
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -------------------------------
# Load API key
# -------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use fast & stable model
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# SYSTEM INSTRUCTION (SCOPE RULES)
# -------------------------------
SYSTEM_PROMPT = """
You are a Career AI Assistant.

You help ONLY with:
- Jobs and internships
- Resume and CV improvement
- Backend / software / data / AI careers
- Interview questions and preparation
- Career skills and guidance

Rules:
- Allow greetings like hello, hi
- If a question is NOT related to careers or tech:
  respond politely with:
  "I'm focused on career and technical guidance. 
   Please ask something related to jobs, resumes, or interviews."
- Be concise and practical
"""

# -------------------------------
# Public function
# -------------------------------
def query_llm(user_prompt: str) -> str:
    """
    Sends prompt to Gemini with system instruction.
    """

    try:
        full_prompt = SYSTEM_PROMPT + "\n\nUser question:\n" + user_prompt
        response = model.generate_content(full_prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ LLM error: {e}"
