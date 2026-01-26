"""
backend/app.py - FastAPI Backend for Career AI Agent
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile
import json
from typing import Optional
from datetime import datetime

# Import your existing modules
from analytics import (
    analyze_resume_for_role,
    detect_skill_gaps,
    calculate_resume_job_match,
    reverse_job_matcher,
    build_star_story,
    company_specific_interview_questions,
    resume_heatmap,
)
from jobs import search_jobs, search_jobs_by_skills
from memory import (
    load_memory, save_memory, set_resume, get_resume_text, 
    is_resume_uploaded, add_to_history, clear_resume,
    set_star_mode, is_star_mode, get_memory_summary,
    clear_memory
)
from llm import query_llm

# ==================== FastAPI App ====================
app = FastAPI(
    title="Career AI Agent API",
    version="1.0",
    description="AI-powered career assistant backend"
)

# CORS setup (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Helper Functions ====================

def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract text from PDF or TXT files"""
    try:
        if filename.lower().endswith('.pdf'):
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text[:3000]  # Limit text length
            
        elif filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[:3000]
                
        else:
            return f"Unsupported file: {filename}"
            
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# ==================== API Routes ====================

@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "Career AI Agent API",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "chat": "/api/chat",
            "upload_resume": "/api/upload-resume",
            "analyze_match": "/api/analyze-match",
            "skill_gaps": "/api/skill-gaps",
            "alternative_roles": "/api/alternative-roles",
            "interview_questions": "/api/interview-questions",
            "heatmap": "/api/heatmap",
            "memory": "/api/memory",
            "jobs": "/api/jobs"
        }
    }

@app.post("/api/chat")
async def chat_endpoint(user_input: str = Form(...)):
    """
    Handle chat messages from frontend
    
    Example: POST /api/chat with form data: user_input="Hello"
    """
    try:
        print(f"📨 Chat received: {user_input[:50]}...")
        
        # Add user message to history
        add_to_history("default", user_input)
        
        # Get current state
        resume_uploaded = is_resume_uploaded()
        resume_text = get_resume_text()
        star_mode = is_star_mode()
        
        text = user_input.lower().strip()
        
        # ===== ROUTING LOGIC =====
        
        # 1. Greetings
        if text in ["hi", "hello", "hey", "greetings"]:
            response = "👋 Hello! I'm your Career AI Assistant. How can I help with your career today?"
        
        # 2. STAR Mode
        elif star_mode:
            response = build_star_story(user_input)
            set_star_mode("default", False)
        
        # 3. Activate STAR mode
        elif "star" in text or "behavioral" in text or "interview story" in text:
            set_star_mode("default", True)
            response = "📝 I'll help you create a STAR interview answer. Please describe your experience or situation."
        
        # 4. Resume-based questions
        elif any(keyword in text for keyword in ["based on my resume", "from my resume", "my resume", "according to my resume"]):
            if not resume_uploaded:
                response = "📄 Please upload your resume first using the upload button on the left."
            else:
                if "job" in text or "jobs" in text or "position" in text or "role" in text:
                    # Search jobs based on resume skills
                    jobs = search_jobs_by_skills(resume_text, "Software Engineer")
                    if jobs:
                        response = "🔍 **Jobs matching your resume:**\n\n" + "\n\n".join(jobs[:3])
                    else:
                        response = "No matching jobs found. Try uploading your resume first."
                elif "improve" in text or "feedback" in text or "better" in text:
                    response = analyze_resume_for_role("Software Engineer")
                elif "interview" in text and "question" in text:
                    response = query_llm(f"Generate interview questions based on this resume:\n{resume_text[:1000]}")
                else:
                    # General resume-based question
                    response = query_llm(f"Based on this resume:\n{resume_text[:1000]}\n\nQuestion: {user_input}")
        
        # 5. Job search
        elif any(k in text for k in ["job", "jobs", "internship", "intern", "position", "opening", "vacancy"]):
            if resume_uploaded and ("suitable" in text or "for me" in text or "matching" in text or "fit" in text):
                # Personalized job search
                jobs = search_jobs_by_skills(resume_text, "Software Engineer")
                response = "🎯 **Jobs matching your profile:**\n\n" + "\n\n".join(jobs) if jobs else "No matching jobs found."
            else:
                # General job search
                jobs = search_jobs(user_input)
                response = "💼 **Job Opportunities:**\n\n" + "\n\n".join(jobs) if jobs else "No jobs found. Try: 'python developer' or 'backend engineer'"
        
        # 6. Default LLM response
        else:
            response = query_llm(user_input)
        
        # Add response to history
        add_to_history("default", user_input, response)
        
        return JSONResponse({
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "response": f"I encountered an error. Please try again. Error: {str(e)}"
        }, status_code=500)

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and process resume file
    
    Example: POST /api/upload-resume with file in form data
    """
    try:
        print(f"📤 Resume upload: {file.filename}")
        
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Extract text
        resume_text = extract_text_from_file(tmp_path, file.filename)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if "Error" in resume_text:
            raise Exception(resume_text)
        
        # Store in memory
        set_resume("default", resume_text, file.filename)
        
        return JSONResponse({
            "success": True,
            "message": f"✅ Resume '{file.filename}' uploaded successfully!",
            "details": f"Extracted {len(resume_text)} characters",
            "filename": file.filename,
            "has_resume": True
        })
        
    except Exception as e:
        print(f"❌ Resume upload error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "message": f"Failed to upload resume: {str(e)}"
        }, status_code=500)

@app.post("/api/analyze-match")
async def analyze_match(job_description: str = Form(...)):
    """
    Calculate resume-job match percentage
    
    Example: POST /api/analyze-match with form data: job_description="..."
    """
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        result = calculate_resume_job_match(job_description)
        
        return JSONResponse({
            "success": True,
            "result": result,
            "type": "match_analysis",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Match analysis error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "result": f"Error analyzing match: {str(e)}"
        }, status_code=500)

@app.post("/api/skill-gaps")
async def skill_gaps(job_description: str = Form(...)):
    """
    Detect skill gaps between resume and job description
    
    Example: POST /api/skill-gaps with form data: job_description="..."
    """
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        result = detect_skill_gaps(job_description)
        
        return JSONResponse({
            "success": True,
            "result": result,
            "type": "skill_gaps",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Skill gaps error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "result": f"Error detecting skill gaps: {str(e)}"
        }, status_code=500)

@app.get("/api/alternative-roles")
async def alternative_roles():
    """
    Suggest alternative/hidden job roles based on resume
    
    Example: GET /api/alternative-roles
    """
    try:
        if not is_resume_uploaded():
            raise HTTPException(status_code=400, detail="Upload resume first")
        
        result = reverse_job_matcher()
        
        return JSONResponse({
            "success": True,
            "result": result,
            "type": "alternative_roles",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Alternative roles error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "result": f"Error finding alternative roles: {str(e)}"
        }, status_code=500)

@app.post("/api/interview-questions")
async def interview_questions(
    company: str = Form(...),
    role: str = Form("Backend Engineer")
):
    """
    Generate company-specific interview questions
    
    Example: POST /api/interview-questions with form data: company="Google", role="Backend Engineer"
    """
    try:
        if not company.strip():
            raise HTTPException(status_code=400, detail="Company information is required")
        
        result = company_specific_interview_questions(company, role)
        
        return JSONResponse({
            "success": True,
            "result": result,
            "type": "interview_questions",
            "company": company,
            "role": role,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Interview questions error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "result": f"Error generating questions: {str(e)}"
        }, status_code=500)

@app.post("/api/heatmap")
async def heatmap(job_description: str = Form(...)):
    """
    Generate resume heatmap vs job description
    
    Example: POST /api/heatmap with form data: job_description="..."
    """
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required")
        
        result = resume_heatmap(job_description)
        
        return JSONResponse({
            "success": True,
            "result": result,
            "type": "resume_heatmap",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Heatmap error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "result": f"Error generating heatmap: {str(e)}"
        }, status_code=500)

@app.get("/api/jobs")
async def get_jobs(query: Optional[str] = None):
    """
    Search for jobs (general or skills-based)
    
    Example: 
    - GET /api/jobs?query=python+developer
    - GET /api/jobs (uses resume if uploaded)
    """
    try:
        resume_uploaded = is_resume_uploaded()
        resume_text = get_resume_text()
        
        if resume_uploaded and not query:
            # Use resume-based search
            jobs = search_jobs_by_skills(resume_text, "Software Engineer")
            return JSONResponse({
                "success": True,
                "jobs": jobs,
                "source": "resume_based",
                "count": len(jobs)
            })
        else:
            # Use query-based search
            search_query = query or "software engineer"
            jobs = search_jobs(search_query)
            return JSONResponse({
                "success": True,
                "jobs": jobs,
                "source": "query_based",
                "query": search_query,
                "count": len(jobs)
            })
            
    except Exception as e:
        print(f"❌ Jobs search error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "jobs": []
        }, status_code=500)

@app.get("/api/memory")
async def get_memory():
    """
    Get current memory state
    
    Example: GET /api/memory
    """
    try:
        memory = load_memory()
        summary = get_memory_summary()
        
        return JSONResponse({
            "success": True,
            "memory": memory,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Memory error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e),
            "memory": {}
        }, status_code=500)

@app.post("/api/clear-memory")
async def clear_memory_endpoint():
    """
    Clear all memory (reset conversation)
    
    Example: POST /api/clear-memory
    """
    try:
        clear_memory("default")
        
        return JSONResponse({
            "success": True,
            "message": "Memory cleared successfully",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Clear memory error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.post("/api/clear-resume")
async def clear_resume_endpoint():
    """
    Clear resume from memory
    
    Example: POST /api/clear-resume
    """
    try:
        clear_resume("default")
        
        return JSONResponse({
            "success": True,
            "message": "Resume cleared from memory",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Clear resume error: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Example: GET /api/health
    """
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Career AI Agent API"
    })

# ==================== Main Execution ====================

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    
    print(" Starting Career AI Agent API...")
    print(" Endpoints:")
    print("  - POST /api/chat           - Chat with AI")
    print("  - POST /api/upload-resume  - Upload resume")
    print("  - POST /api/analyze-match  - Match percentage")
    print("  - POST /api/skill-gaps     - Skill gap analysis")
    print("  - GET  /api/alternative-roles - Alternative roles")
    print("  - POST /api/heatmap        - Resume heatmap")
    print("  - GET  /api/health         - Health check")
    print("\n Server running on http://localhost:8000")
    

