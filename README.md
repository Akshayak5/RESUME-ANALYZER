## 💡RESUMEIQ (RESUME-ANALYZER)

ResumeIQ is a web-based application designed to automate and enhance the process of resume evaluation using Natural Language Processing (NLP) and AI techniques. The system allows users to upload resumes in multiple formats such as PDF, DOCX, DOC, and TXT, and extracts essential information including candidate details, skills, and experience.

The application analyzes the extracted data to generate a resume score based on industry-relevant parameters such as skill diversity, demand, and completeness. It identifies missing or in-demand skills and provides actionable suggestions to help candidates improve their resumes and increase their employability.

In addition, the system offers job role recommendations by matching candidate skills with industry roles and calculating a match percentage. A unique skill verification module enables users to validate their abilities through short tests, with verified skills highlighted to improve credibility.

The platform also includes advanced features such as resume history tracking, trending skills analysis, and a career roadmap generator, which provides insights into required skills, learning paths, estimated time to achieve job readiness, and expected salary ranges.

An AI Resume Enhancer, powered by advanced AI models, improves resume quality by correcting errors, refining content, and generating stronger bullet points. Users can download the enhanced resume for further use.

For recruiters, the system provides an employer search module that enables efficient candidate filtering based on skills, scores, and experience, along with options to shortlist and export candidate data.

Overall, the AI Resume Analyzer streamlines resume screening, assists candidates in building stronger profiles, and helps recruiters identify suitable talent efficiently, making it a comprehensive solution for modern recruitment and career development.


## ✨Features

	•	Resume Upload & Parsing
        Upload resumes in multiple formats such as PDF, DOCX, DOC, and TXT. The system automatically extracts relevant information from the uploaded resume.
		
	•	Automatic Skill Extraction
        Uses Natural Language Processing (NLP) to identify technical skills and keywords from the resume content.
		
	•	Resume Scoring System
        Generates a resume score based on factors such as the number of skills, skill diversity, and industry-demanded technologies.
		
	•	Missing Skill Identification
        Detects skills that are commonly required in the industry but are missing from the resume, helping candidates improve their profiles.
		
	•	Job Role Recommendations
        Suggests suitable job roles based on the candidate’s skills and experience, along with a match percentage.
		
	•	Skill Verification Tests
        Allows candidates to take short skill-based tests to validate their abilities and display verified skills in their profile.
		
	•	Employer Candidate Search
        Enables recruiters to search and filter candidates based on skills, resume scores, or verified abilities.
		
	•	Trending Skills Analysis
        Displays frequently occurring skills from analyzed resumes to highlight current industry trends.
		
	•	Resume History Tracking
        Stores previously analyzed resumes so users can view and compare their past analysis results.

	•	Career Roadmap
        Allows candidates to enter a target job role and receive an AI-generated roadmap showing current match percentage, skills already acquired, skills to learn, estimated time to job-readiness, and expected salary range — with role suggestions across Tech, Healthcare, Business, and Engineering domains.
		
    •	AI Resume Enhancer
        Powered by Groq AI, it fixes spelling errors, rephrases weak bullet points, removes weak phrases, and provides improvement tips. Displays a fully enhanced resume that can be copied or downloaded as a DOCX file.

		
## 🛠️Tech Stack

Frontend


	•	HTML5
	•	CSS3
	•	JavaScript

Backend

	•	Python
	•	Flask
	•	Flask-CORS
	•	Werkzeug

Database

	•	MongoDB

NLP & Resume Processing

	•	spaCy (Natural Language Processing)
	•	pdfplumber (PDF text extraction)
	•	python-docx (DOCX parsing)
	•	Regular Expressions (Regex)

DevOps & Deployment

	•	Docker
	•	Docker Compose
	•	Gunicorn


## 🚀Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git
 
### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
cd resume-analyzer
```
 
### 2. Set up environment variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb://mongo:27017/resumeiq
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=0
```
 
### 3. Build and run with Docker
```bash
docker-compose up --build
```
 
### 4. Access the app
| Service | URL |
|---|---|
| Frontend | http://localhost:5000 |
| Mongo Express | http://localhost:8081 |
 
---
 
## 📁 Project Structure
 
```
resume-analyzer/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── backend/
│   ├── __init__.py
│   ├── app.py                  # Flask app entry point
│   ├── requirements.txt
│   ├── .env
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # MongoDB document schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── resume_routes.py    # Resume API endpoints
│   │   ├── auth_routes.py      # Auth API endpoints
│   │   └── employer_routes.py  # Employer API endpoints
│   └── utils/
│       ├── nlp_engine.py
│       └── resume_parser.py
├── docker/
│   └── mongo-init.js
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── dashboard.css
│   │   │   └── main.css
│   │   └── js/
│   │       ├── api.js
│   │       └── dashboard.js
│   └── templates/
│       ├── dashboard.html
│       ├── employer.html
│       ├── index.html
│       └── reset-password.html
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```
 
---
 
## 📡 API Endpoints
 
### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get user info |
| GET | `/api/auth/profile/:uid` | Get user profile |
 
### Resume
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resume/analyze` | Upload and analyze a resume |
| GET | `/api/resume/:id` | Get a specific resume |
| GET | `/api/resume/history?user_id=` | Get resume history for a user |
| POST | `/api/resume/verify-skill` | Submit a skill verification test |
| GET | `/api/resume/skills/trending` | Get trending skills across all resumes |
 
### Employer
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/employer/candidates` | Browse all candidates |
 
---
 
## 🧪 Testing the API
 
Import the Postman collection from `postman/ResumeIQ_API.postman_collection.json` to test all endpoints.
 
---
 
## 🔄 CI/CD
 
This project uses **GitHub Actions** for automated build and deployment. The workflow is defined in `.github/workflows/ci-cd.yml`.
 
---
 
## 🤝 Contributing
 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
 
---
 
## 📄 License
 
This project is licensed under the MIT License.
 
---
 
## 👨‍💻 Author
 
Built with ❤️ by **Akshaya**
 
