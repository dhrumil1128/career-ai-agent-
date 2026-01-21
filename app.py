"""
app.py
------
Main application entry point for Career AI Agent.

Responsibilities:
- Build Gradio UI
- Route user input to correct intelligence function
- Store & display memory
- Keep UI simple, fast, and professional

ALL intelligence lives in:
- llm.py
- analytics.py
- resume.py
- jobs.py
- memory.py
"""

import gradio as gr
from datetime import datetime

# ===============================
# Internal modules
# ===============================
from llm import query_llm
from memory import load_memory, save_memory
from resume import analyze_resume
from jobs import search_jobs

from analytics import (
    analyze_resume_for_role,
    detect_skill_gaps,
    calculate_resume_job_match,
    reverse_job_matcher,
    build_star_story,
    company_specific_interview_questions,
    resume_heatmap,

)

# ===============================
# App metadata
# ===============================
APP_TITLE = "Career AI Agent"
APP_TAGLINE = "AI-powered career assistant for jobs, resumes & interviews"


# ===============================
# CENTRAL AGENT CONTROLLER
# ===============================
def agent_controller(user_input, chat_history):
    """
    Central brain of the app.

    Keyword-based routing only.
    No hard blocking. LLM is guided via system prompt.
    """
    memory = load_memory()
    star_mode = memory.get("star_mode", False)

    

    memory.setdefault("history", []).append({
        "time": datetime.utcnow().isoformat(),
        "user": user_input
    })

    text = user_input.lower().strip()

    # ---- Friendly greetings ----
    if text in ["hi", "hello", "hey"]:
        response = "Hello 👋 How can I help you with your career today?"

    elif star_mode:
        response = build_star_story(user_input)

        memory["star_mode"] = False
        save_memory("default", memory)

    # ---- STAR story builder ----
    elif "star" in text or "behavioral" in text:
        memory["star_mode"] = True
        save_memory("default", memory)

        response = (
        "Great 👍\n\n"
        "Please describe your experience or project in your own words.\n"
        "I’ll convert it into a STAR interview answer."
        )
      # ---- Resume improvement ----
    elif "improve" in text and "resume" in text:
        response = analyze_resume_for_role("Backend Engineer")

    # ---- Interview questions ----
    elif "interview" in text and "question" in text:
        prompt = f"""
        You are a technical interviewer.

        Generate 5 interview questions for:
        {user_input}

        Rules:
        - Questions only
        - No explanations
        """
        response = query_llm(prompt)

    

    # ---- Job search ----
    elif any(k in text for k in ["job", "jobs", "internship", "intern"]):
        jobs = search_jobs(user_input)
        response = (
            "🔎 **Top matching opportunities:**\n\n" +
            "\n".join(f"- {job}" for job in jobs)
        ) if jobs else "⚠️ No matching jobs found."

    # ---- Default (career LLM) ----
    else:
        response = query_llm(user_input)

    memory["last_response"] = response
    save_memory("default", memory)

    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

    return chat_history, load_memory(), ""


# ===============================
# RESUME UPLOAD HANDLER
# ===============================
def resume_handler(file_path):
    if not file_path:
        return [], load_memory()

    analysis = analyze_resume(file_path)
    return [{"role": "assistant", "content": analysis}], load_memory()


# ===============================
# RESUME ↔ JOB MATCH HANDLERS
# ===============================
def match_percentage_handler(jd_text, chat_history):
    result = calculate_resume_job_match(jd_text)

    chat_history = chat_history or []
    chat_history.append({
        "role": "assistant",
        "content": result
    })

    return chat_history


def skill_gap_handler(jd_text, chat_history):
    result = detect_skill_gaps(jd_text)

    chat_history = chat_history or []
    chat_history.append({
        "role": "assistant",
        "content": result
    })

    return chat_history


def reverse_match_handler(chat_history):
    result = reverse_job_matcher()

    chat_history = chat_history or []
    chat_history.append({
        "role": "assistant",
        "content": result
    })

    return chat_history



def company_interview_handler(company_text, role, chat_history):
    questions = company_specific_interview_questions(company_text, role)

    chat_history = chat_history or []
    chat_history.append({
        "role": "assistant",
        "content": f"🏢 **Company-Specific Interview Questions**\n\n{questions}"
    })

    return chat_history



def heatmap_handler(jd_text, chat_history):
    chat_history = chat_history or []

    text_result = resume_heatmap(jd_text)

    chat_history.append({
        "role": "assistant",
        "content": text_result
    })

    return chat_history













# ===============================
# UI (Gradio)
# ===============================
with gr.Blocks() as demo:
    gr.Markdown(f"## {APP_TITLE}")
    gr.Markdown(APP_TAGLINE)

    with gr.Row():

        # =========================
        # LEFT SIDEBAR
        # =========================
        with gr.Column(scale=1):

            # ---- Memory ----
            gr.Markdown("### 🧠 Memory")
            memory_view = gr.JSON(value=load_memory())

            # ---- Resume Upload ----
            gr.Markdown("### 📄 Resume")
            resume_file = gr.File(
                label="Upload Resume (PDF)",
                type="filepath"
            )
            analyze_btn = gr.Button("Analyze Resume")

            # ---- Job Description Tools ----
            gr.Markdown("### 📌 Job Description")
            jd_input = gr.Textbox(
                placeholder="Paste Job Description here...",
                lines=8
            )

            match_btn = gr.Button("📊 Calculate Match %")
            gap_btn = gr.Button("🧠 Show Skill Gaps")
            reverse_btn = gr.Button("🔁 Suggest Alternative Roles")
            heatmap_btn = gr.Button("🔥 Resume Heatmap")


            # ---- Company Interview Prep ----
            gr.Markdown("### 🏢 Company-Specific Interview Prep")

            company_input = gr.Textbox(
                label="Company Info / About Page / JD",
                placeholder="Paste company description, news, or JD...",
                lines=6
            )

            role_input = gr.Textbox(
                label="Target Role",
                value="Backend Engineer"
            )

            company_interview_btn = gr.Button(
                "🎯 Generate Company Interview Questions"
            )

        # =========================
        # MAIN CHAT AREA
        # =========================
        with gr.Column(scale=3):

            chatbot = gr.Chatbot(height=420)

        

            user_input = gr.Textbox(
            placeholder="Ask about jobs, resumes, or interviews..."
        )

            send_btn = gr.Button("Send", variant="primary")

            
            


    # ===============================
    # Wiring
    # ===============================
    send_btn.click(
        agent_controller,
        [user_input, chatbot],
        [chatbot, memory_view, user_input]
    )

    user_input.submit(
        agent_controller,
        [user_input, chatbot],
        [chatbot, memory_view, user_input]
    )

    analyze_btn.click(
        resume_handler,
        resume_file,
        [chatbot, memory_view]
    )

    match_btn.click(
        match_percentage_handler,
        [jd_input, chatbot],
        chatbot
    )

    gap_btn.click(
        skill_gap_handler,
        [jd_input, chatbot],
        chatbot
    )

    reverse_btn.click(
        reverse_match_handler,
        chatbot,
        chatbot
    )

    company_interview_btn.click(
        company_interview_handler,
        [company_input, role_input, chatbot],
        chatbot
    )

    
 
    
    heatmap_btn.click(
        heatmap_handler,
        inputs=[jd_input, chatbot],
        outputs=[chatbot]
    )



# ===============================
# Launch
# ===============================
demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)
