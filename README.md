# Career AI Agent

##  Project Overview

**Career AI Agent** is an intelligent career assistant that helps job seekers find opportunities, improve resumes, prepare for interviews, and identify skill gaps using AI. It combines LinkedIn job search with Gemini AI for personalized career guidance.

---

##  Problem Solved

Job seekers often struggle with:

* Finding relevant job opportunities
* Understanding resume weaknesses
* Preparing for company-specific interviews
* Identifying missing skills for target roles
* Getting personalized career advice

**Our Solution:** An AI-powered platform that provides all career services in one place with real-time job data and personalized AI analysis.

---

##  Tech Stack

###  Backend

* **FastAPI** – Modern Python web framework
* **Gemini AI (Google)** – Intelligent career analysis
* **BeautifulSoup4** – Web scraping LinkedIn jobs
* **pdfplumber** – Resume PDF text extraction
* **Python-dotenv** – Environment management
* **Uvicorn** – ASGI server

###  Frontend

* **HTML5** – Structure
* **CSS3 (Gradient Themes)** – Styling
* **JavaScript (ES6+)** – Interactive functionality
* **Bootstrap 5** – Responsive components
* **Font Awesome** – Icons

###  APIs & Services

* **LinkedIn Public Jobs API** – Real job listings
* **Gemini API** – AI-powered career insights
* **Custom REST API** – Backend communication

---

## Key Features

### 1.  Intelligent Chat Assistant

* Natural language career conversations
* Context-aware responses with memory
* Resume-based personalized advice
* STAR interview story builder

### 2.  Resume Analysis & Improvement

* Upload PDF/TXT resumes
* Analyze against target roles
* Identify weak sections
* Suggest concrete improvements
* Automatic skill extraction

### 3.  Smart Job Search

* Real-time LinkedIn job listings
* Resume-based skill matching
* Company-specific opportunities
* Direct LinkedIn apply links
* Location & remote filters

### 4.  Job Description Analysis

* **Match Percentage** – Resume vs JD compatibility
* **Skill Gap Detection** – Top 3 missing skills
* **Resume Heatmap** – Section-by-section visual analysis
* **Learning Recommendations** – How to fill gaps

### 5.  Alternative Career Paths

* Hidden role discovery
* Transferable skills analysis
* Career progression suggestions
* Industry transition guidance

### 6.  Interview Preparation

* Company-specific interview questions
* Technical & behavioral question sets
* Role-tailored interview practice
* STAR method story polishing

### 7.  Memory System

* Conversation history
* Resume storage (one-time upload)
* User preferences
* Session management (multi-user support)

---

##  Project Structure

```
career-ai-agent/
├── backend/
│   ├── app.py              # FastAPI server (NO GRADIO)
│   ├── analytics.py        # AI analysis functions
│   ├── jobs.py             # LinkedIn job search
│   ├── llm.py              # Gemini AI integration
│   ├── memory.py           # User memory system
│   ├── requirements.txt    # Python dependencies
│   └── .env                # API keys (gitignored)
│
├── frontend/
│   ├── index.html          # Main UI with Bootstrap
│   ├── style.css           # Gradient-based modern styling
│   ├── script.js           # Frontend logic
│   └── assets/             # Images & icons
│
└── README.md               # Project documentation
```

---

##  Quick Start

### 1️. Clone & Setup

```bash
git clone <repository-url>
cd career-ai-agent
cd backend
pip install -r requirements.txt
```

### 2️. Configure API Keys

Create `backend/.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
# LinkedIn does not require API keys (public search)
```

Get Gemini API key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 3️. Run Backend

```bash
cd backend
python app.py
```

 Runs at: **[http://localhost:8000](http://localhost:8000)**

### 4️. Run Frontend

```bash
cd frontend
python -m http.server 3000
```

 Runs at: **[http://localhost:3000](http://localhost:3000)**

### 5️. Open Browser

Go to: **[http://localhost:3000](http://localhost:3000)**

---

##  Usage Guide

### Step 1: Upload Resume

* Click **"Choose File"** in sidebar
* Select PDF/TXT resume
* Click **"Upload & Analyze"**
* Resume is stored and analyzed by AI

### Step 2: Ask Career Questions

Example prompts:

* "Find jobs based on my resume"
* "How can I improve my resume for backend roles?"
* "What are my key skills?"
* "Prepare me for Google interviews"

### Step 3: Analyze Job Descriptions

* Paste job description in sidebar
* Click:

  * **Match %** – Compatibility score
  * **Skill Gaps** – Missing skills
  * **Heatmap** – Visual analysis

### Step 4: Get Interview Ready

* Enter company name & role
* Click **"Generate Questions"**
* Get tailored technical & behavioral questions

---

## 🔧 API Endpoints

| Method | Endpoint                   | Description                |
| ------ | -------------------------- | -------------------------- |
| POST   | `/api/chat`                | AI career chat             |
| POST   | `/api/upload-resume`       | Upload resume              |
| POST   | `/api/analyze-match`       | Resume-JD match %          |
| POST   | `/api/skill-gaps`          | Detect missing skills      |
| GET    | `/api/alternative-roles`   | Suggest alternative roles  |
| POST   | `/api/interview-questions` | Company-specific questions |
| POST   | `/api/heatmap`             | Resume visual analysis     |
| GET    | `/api/jobs`                | Job search                 |
| GET    | `/api/memory`              | View user memory           |

---

##  UI Features

* Modern gradient-based design
* Responsive layout (mobile & desktop)
* Dark theme for eye comfort
* Real-time chat experience
* Interactive sidebar navigation
* Drag & drop file upload

---

##  Business Value

* **Job Seekers:** All-in-one career platform
* **Recruiters:** Better-prepared candidates
* **Companies:** Higher interview success rates
* **Educators:** Career guidance & mentoring tool

---

##  Privacy & Security

* Local processing – resume stays on your server
* No data selling
* Encrypted storage
* Optional cloud deployment

---

##  Future Enhancements

* AI-powered cover letter generator
* Salary negotiation assistant
* Career path visualization
* Networking strategy builder
* Interview performance analytics
* Multiple resume versions
* Job application tracker
* Industry trend analysis

---

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to branch
5. Open a Pull Request

---

##  License

MIT License – See `LICENSE` file

---

## Author

**Dhrumil Pawar**
Career AI Agent Developer

---

##  Support

If you found this useful, give it a  and share it!
