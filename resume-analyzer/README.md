# ⚡ ResumeAI — AI Resume Analyzer with Skill Verification

A full-stack web application that analyzes resumes using NLP, calculates resume scores, detects skills, recommends job roles, and lets users verify their skills through quizzes.

---

## 📁 Project Structure

```
resume-analyzer/
├── backend/                    # Flask API
│   ├── app.py                  # Entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── auth_routes.py      # Register / Login / Profile
│   │   ├── resume_routes.py    # Upload / Analyze / History
│   │   ├── quiz_routes.py      # Skill Quiz / Submit / Verified
│   │   └── dashboard_routes.py # Stats / Activity / Progress
│   ├── models/
│   │   ├── user_model.py       # User CRUD + password hashing
│   │   ├── resume_model.py     # Resume storage & retrieval
│   │   └── skill_verification_model.py
│   ├── nlp/
│   │   └── extractor.py        # spaCy NLP pipeline
│   ├── utils/
│   │   └── parser.py           # PDF/DOCX/TXT parsing
│   ├── middleware/
│   │   └── auth_middleware.py
│   └── database/
│       └── connection.py       # MongoDB connection & indexes
│
├── frontend/                   # Vanilla HTML/CSS/JS
│   ├── index.html              # Landing page
│   ├── css/main.css            # Full design system
│   ├── js/main.js              # API client + utilities
│   └── pages/
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── analyze.html        # Upload + Results
│       ├── history.html        # Resume history table
│       ├── quiz.html           # Skill verification
│       └── profile.html
│
├── database/
│   └── seeds/seed.py           # Sample data seeder
│
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone / extract the project
cd resume-analyzer

# Start all services (MongoDB + Backend + Frontend)
docker-compose up --build

# Seed demo data
docker exec resumeai_backend python /app/../database/seeds/seed.py
```

Then open: http://localhost:3000

Demo login: `demo@resumeai.dev` / `demo1234`

---

### Option 2: Manual Setup

#### 1. Start MongoDB
```bash
# Install MongoDB locally or use MongoDB Atlas
# Default: mongodb://localhost:27017/
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy NLP model
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and secret keys

# Run the API
python app.py
# → Backend running at http://localhost:5000
```

#### 3. Frontend Setup
```bash
cd frontend

# Option A: Open directly in browser
open index.html

# Option B: Use a local dev server (recommended)
npx serve .   # or: python -m http.server 3000
# → Frontend at http://localhost:3000
```

#### 4. Seed Database (optional)
```bash
cd resume-analyzer
python database/seeds/seed.py
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/profile` | Update profile |

### Resume
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/upload` | Upload & analyze file |
| POST | `/api/resume/analyze-text` | Analyze pasted text |
| GET | `/api/resume/history` | Get all user resumes |
| GET | `/api/resume/:id` | Get single resume |
| DELETE | `/api/resume/:id` | Delete resume |

### Quiz
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/quiz/questions/:skill` | Get quiz questions |
| POST | `/api/quiz/submit` | Submit answers |
| GET | `/api/quiz/verified` | Get verified skills |
| GET | `/api/quiz/available-skills` | List all quizzable skills |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Resume & verification stats |
| GET | `/api/dashboard/recent-activity` | Recent events |
| GET | `/api/dashboard/progress` | Score progress over time |

---

## 🧠 NLP Features

The `nlp/extractor.py` module uses **spaCy** + keyword matching to:
- Detect 50+ technical skills across 9 categories
- Estimate years of experience with regex patterns
- Identify education level (PhD, Master's, Bachelor's, etc.)
- Extract contact information (email, phone, name)
- Calculate resume score with 4-category breakdown
- Recommend job roles based on skill match

---

## 🗄️ MongoDB Collections

| Collection | Description |
|------------|-------------|
| `users` | Account info, verified skills, profile |
| `resumes` | Uploaded resumes with full NLP analysis |
| `skill_verifications` | Quiz attempts and results |

---

## ✅ Supported File Types
- **PDF** — via `pdfplumber`
- **DOCX** — via `python-docx`
- **TXT** — native Python

---

## 🛠️ Technologies

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.11, Flask 3.0 |
| Database | MongoDB 7.0, PyMongo |
| NLP | spaCy (en_core_web_sm) |
| Auth | Flask-JWT-Extended, bcrypt |
| Parsing | pdfplumber, python-docx |
| DevOps | Docker, Docker Compose, Nginx |

---

## 🔐 Security
- Passwords hashed with bcrypt
- JWT tokens with 7-day expiry
- File uploads validated by extension
- All resume routes require authentication
- Unique email enforcement at DB level
