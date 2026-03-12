## RESUME-ANLYZER

The AI Resume Analyzer is a web-based application that analyzes resumes using Natural Language Processing (NLP) techniques to extract important information such as candidate details, skills, and experience. The system evaluates the extracted data and generates a resume score based on industry-relevant skill requirements.

The application also identifies missing skills and provides suggestions to help candidates improve their profiles. Additionally, it recommends suitable job roles by matching the candidate’s skill set with common industry roles and displaying a match percentage.

The platform includes a skill verification feature, allowing candidates to validate their abilities through short tests. Verified skills are highlighted, making it easier for recruiters to identify qualified candidates.

Furthermore, the system provides an employer search module that enables recruiters to filter and find potential candidates based on specific skills and resume scores. Overall, the AI Resume Analyzer helps streamline resume evaluation, assists candidates in improving their resumes, and supports recruiters in efficiently identifying suitable talent.


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

