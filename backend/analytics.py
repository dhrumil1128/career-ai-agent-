"""
analytics.py
-------------
This module contains ALL advanced intelligence for the Career AI Agent.

Purpose:
- Deep resume understanding
- Resume ↔ Job matching
- Skill gap detection
- Reverse job matching (hidden roles)
- Interview & career insights

IMPORTANT:
- No UI code here
- No Gradio imports
- Pure intelligence & reasoning layer
"""

from llm import query_llm
from memory import load_memory
import re









# ==========================================================
# 1️⃣ Resume Improvement for a Target Role
# ==========================================================

def analyze_resume_for_role(target_role: str):
    """
    Analyzes the user's resume for a specific role
    and suggests improvements.

    Example:
    - Backend Engineer
    - Data Engineer
    """

    memory = load_memory()
    resume_text = memory.get("resume_text")

    if not resume_text:
        return "📄 Please upload your resume first."

    prompt = f"""
You are a senior technical recruiter.

Resume:
{resume_text}

Target Role:
{target_role}

Task:
- Identify weak sections
- Suggest concrete improvements
- Mention missing skills or experience
- Keep suggestions actionable

Output format:
- Bullet points only
- Clear and concise
"""

    return query_llm(prompt)


# ==========================================================
# 2️⃣ Skill Gap Agent (Resume vs Job Description)
# ==========================================================

def detect_skill_gaps(job_description: str):
    """
    Compares resume with a job description
    and identifies the TOP 3 missing or weak skills.
    """

    memory = load_memory()
    resume_text = memory.get("resume_text")

    if not resume_text:
        return "📄 Please upload your resume first."

    prompt = f"""
You are an AI hiring analyst.

Resume:
{resume_text}

Job Description:
{job_description}

Task:
- Identify the TOP 3 missing or weak skills
- Explain WHY each skill matters
- Suggest HOW to learn or improve each skill

Rules:
- No fluff
- Career-focused
- Practical advice
"""

    return query_llm(prompt)


# ==========================================================
# 3️⃣ Resume ↔ Job Match Percentage
# ==========================================================

def calculate_resume_job_match(job_description: str):
    """
    Calculates how well the resume matches a job description.
    Returns percentage + explanation.
    """

    memory = load_memory()
    resume_text = memory.get("resume_text")

    if not resume_text:
        return "📄 Please upload your resume first."

    prompt = f"""
You are an ATS (Applicant Tracking System).

Resume:
{resume_text}

Job Description:
{job_description}

Task:
- Give a match percentage (0–100%)
- Explain strengths
- Explain gaps

Output format:
Match Percentage: XX%
Strengths:
- ...
Gaps:
- ...
"""

    return query_llm(prompt)


# ==========================================================
# 4️⃣ Reverse Job Matcher (🔥 UNIQUE FEATURE)
# ==========================================================

def reverse_job_matcher():
    """
    Suggests alternative / hidden job roles
    the user is suited for based on their resume.
    """

    memory = load_memory()
    resume_text = memory.get("resume_text")

    if not resume_text:
        return "📄 Please upload your resume first."

    prompt = f"""
You are a career strategist.

Resume:
{resume_text}

Task:
- Identify hidden strengths
- Infer transferable skills
- Suggest 3 alternative job roles the user
  may not be actively searching for

For each role:
- Why they are a good fit
- What to improve to transition into it

Rules:
- Do NOT repeat obvious roles
- Focus on career growth
"""

    return query_llm(prompt)


# ==========================================================
# 5️⃣ STAR Story Builder (Behavioral Interview)
# ==========================================================

def build_star_story(raw_story: str):
    """
    Converts a messy experience into a
    polished STAR interview answer.
    """

    prompt = f"""
You are an interview coach.

User's raw story:
{raw_story}

Task:
- Extract Situation
- Extract Task
- Extract Action
- Extract Result

Then generate:
- A polished 30-second interview answer
- Clear, confident, professional tone
"""

    return query_llm(prompt)



# ==========================================================
# 6 STAR Story Builder (Behavioral Interview)
# ==========================================================
def company_specific_interview_questions(company_context: str, role: str = "Backend Engineer"):
    """
    Generates interview questions tailored to a specific company.
    
    company_context:
    - Company name OR
    - About Us text OR
    - JD text
    """

    memory = load_memory()
    resume_text = memory.get("resume_text", "")

    prompt = f"""
You are a senior interviewer at the following company:

{company_context}

You are interviewing a candidate for the role of {role}.

Candidate resume (if available):
{resume_text}

Generate:
- 5 technical interview questions
- 2 system design questions
- 2 behavioral questions

Rules:
- Questions only
- No explanations
- Company-specific context is REQUIRED
"""

    return query_llm(prompt)






# ==========================================================
# 7  HeatMap 
# ==========================================================

# ==========================================================
# 7️⃣ Resume Heatmap (Single Source of Truth)
# ==========================================================

def resume_heatmap(jd_text):
    """
    Returns a chatbot-friendly resume heatmap
    with progress bars and explanations.
    """

    memory = load_memory()
    resume_text = memory.get("resume_text")

    if not resume_text:
        return "📄 Please upload your resume first."

    prompt = f"""
You are an ATS + career expert.

Compare each resume section against the job description.

Resume:
{resume_text}

Job Description:
{jd_text}

Return output ONLY in this format:

Section | Score | Explanation

Rules:
- Score between 0 and 100
- One section per line
- No extra text
"""

    result = query_llm(prompt)

    heatmap_lines = []

    for line in result.splitlines():
        if "|" not in line:
            continue

        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 3:
            continue

        section, score_text, explanation = parts

        if section.lower() in ["section", "score", "---"]:
            continue

        match = re.search(r"\d{1,3}", score_text)
        score = int(match.group()) if match else 0
        score = max(0, min(score, 100))

        filled = score // 10
        bar = "●" * filled + "○" * (10 - filled)


        if score >= 75:
            icon = "🟢"
            verdict = "Strong match"
        elif score >= 40:
            icon = "🟡"
            verdict = "Partial match"
        else:
            icon = "🔴"
            verdict = "Weak match"

        heatmap_lines.append(
            f"{icon} **{section.upper()}**\n"
            f"{bar}  **{score}% — {verdict}**\n"
            f"_{explanation}_\n"
)


    if not heatmap_lines:
        return "⚠️ Could not generate heatmap."

    return (
        "📊 **Resume Heatmap vs Job Description**\n\n"
        + "\n".join(heatmap_lines)
    )






