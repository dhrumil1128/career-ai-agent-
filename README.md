Career AI Agent 🚀
📌 Project Overview
Career AI Agent is an intelligent career assistant that helps job seekers find opportunities, improve resumes, prepare for interviews, and identify skill gaps using AI. It combines LinkedIn job search with Gemini AI for personalized career guidance.

🎯 Problem Solved
Job seekers struggle with:

Finding relevant job opportunities

Understanding resume weaknesses

Preparing for company-specific interviews

Identifying missing skills for target roles

Getting personalized career advice

Our Solution: An AI-powered platform that provides all career services in one place with real-time job data and personalized AI analysis.

🛠️ Tech Stack
Backend
FastAPI - Modern Python web framework

Gemini AI (Google) - For intelligent career analysis

BeautifulSoup4 - Web scraping LinkedIn jobs

pdfplumber - Resume PDF text extraction

Python-dotenv - Environment management

Uvicorn - ASGI server

Frontend
HTML5 - Structure

CSS3 with Gradient Themes - Styling

JavaScript (ES6+) - Interactive functionality

Bootstrap 5 - Responsive components

Font Awesome - Icons

APIs & Services
LinkedIn Public Jobs API - Real job listings

Gemini API - AI-powered career insights

Custom REST API - Backend communication

🌟 Key Features
1. 🤖 Intelligent Chat Assistant
Natural language conversations about careers

Context-aware responses using memory

Resume-based personalized advice

STAR interview story builder

2. 📄 Resume Analysis & Improvement
Upload PDF/TXT resumes

Analyze against target roles

Identify weak sections

Suggest concrete improvements

Extract skills automatically

3. 🔍 Smart Job Search
Real-time LinkedIn job listings

Skills-based matching from resume

Company-specific opportunities

Direct LinkedIn apply links

Location & remote filters

4. 📊 Job Description Analysis
Match Percentage - Resume vs JD compatibility

Skill Gap Detection - Top 3 missing skills

Resume Heatmap - Visual section-by-section analysis

Learning Recommendations - How to fill gaps

5. 🎯 Alternative Career Paths
Hidden Role Discovery - Jobs you didn't consider

Transferable Skills analysis

Career Progression suggestions

Industry Transition guidance

6. 🏢 Interview Preparation
Company-specific questions

Technical & Behavioral question sets

Role-tailored interview practice

STAR Method story polishing

7. 💾 Memory System
Conversation History - Remembers context

Resume Storage - One-time upload

User Preferences - Personalized experience

Session Management - Multi-user support

📁 Project Structure
text
career-ai-agent/
├── backend/
│   ├── app.py              # FastAPI server (NO GRADIO)
│   ├── analytics.py        # All AI analysis functions
│   ├── jobs.py            # LinkedIn job search
│   ├── llm.py             # Gemini AI integration
│   ├── memory.py          # User memory system
│   ├── requirements.txt   # Python dependencies
│   └── .env              # API keys (gitignored)
│
├── frontend/
│   ├── index.html         # Main UI with Bootstrap
│   ├── style.css          # Modern gradient styling
│   ├── script.js          # Frontend logic
│   └── assets/           # Images/icons
│
└── README.md             # This file
⚡ Quick Start
1. Clone & Setup
bash
git clone <repository-url>
cd career-ai-agent
cd backend
pip install -r requirements.txt
2. Configure API Keys
Create backend/.env:

env
GEMINI_API_KEY=your_gemini_api_key_here
# LinkedIn doesn't need API keys (public search)
Get Gemini API key: https://makersuite.google.com/app/apikey

3. Run Backend
bash
cd backend
python app.py
➡️ Runs at: http://localhost:8000

4. Run Frontend
bash
cd frontend
python -m http.server 3000
➡️ Runs at: http://localhost:3000

5. Open Browser
Go to: http://localhost:3000

🚀 Usage Guide
Step 1: Upload Resume
Click "Choose File" in sidebar

Select PDF/TXT resume

Click "Upload & Analyze"

AI will store and analyze your resume

Step 2: Ask Career Questions
Chat examples:

"Find jobs based on my resume"

"How can I improve my resume for backend roles?"

"What are my key skills?"

"Prepare me for Google interviews"

Step 3: Analyze Job Descriptions
Paste job description in left sidebar

Click:

Match % - Compatibility score

Skill Gaps - Missing skills

Heatmap - Visual analysis

Step 4: Get Interview Ready
Enter company name and role

Click "Generate Questions"

Get technical + behavioral questions

🔧 API Endpoints
Method	Endpoint	Description
POST	/api/chat	AI career chat
POST	/api/upload-resume	Upload resume
POST	/api/analyze-match	Resume-JD match %
POST	/api/skill-gaps	Detect missing skills
GET	/api/alternative-roles	Suggest hidden roles
POST	/api/interview-questions	Company-specific Qs
POST	/api/heatmap	Visual resume analysis
GET	/api/jobs	Search jobs
GET	/api/memory	View user memory
🎨 UI Features
Modern Gradient Design - Professional look

Responsive Layout - Mobile & desktop

Dark Theme - Easy on eyes

Real-time Chat - Smooth animations

Interactive Sidebar - All tools accessible

File Upload - Drag & drop support

📈 Business Value
For Job Seekers: All-in-one career platform

For Recruiters: Better candidate preparation

For Companies: Higher interview success rates

For Educators: Career guidance tool

🔒 Privacy & Security
Local Processing - Resume stays on your server

No Data Selling - Your data is yours

Encrypted Storage - Secure memory system

Optional Cloud - Can be deployed anywhere

🚀 Future Enhancements
AI-powered cover letter generator

Salary negotiation assistant

Career path visualization

Networking strategy builder

Interview performance analytics

Multiple resume versions

Job application tracker

Industry trend analysis

🤝 Contributing
Fork the repository

Create feature branch

Commit changes

Push to branch

Open Pull Request

📄 License
MIT License - See LICENSE file

👨‍💻 Author
Dhrumil Pawar - Career AI Agent Developer

⭐ Support
Found this useful? Give it a star! ⭐

