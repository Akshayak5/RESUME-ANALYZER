## RESUME-ANLYZER

The AI Resume Analyzer is a web-based application that automatically analyzes resumes using Natural Language Processing (NLP) techniques. It extracts key information such as candidate details, skills, and experience from uploaded resumes and evaluates them against industry-relevant skill requirements.

The system generates a resume score, identifies missing skills, and recommends suitable job roles based on the candidate’s skill set. Additionally, the platform includes a skill verification feature that allows candidates to prove their expertise through tests, helping employers identify verified skills more easily.

The application also provides an employer search system, enabling recruiters to find potential candidates by filtering resumes based on skills and scores.

This platform aims to simplify resume screening, improve candidate profiles, and assist employers in efficient talent discovery


## Features

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


## Tech Stack

Frontend
	•	React.js
	•	HTML
	•	CSS
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

