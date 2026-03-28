"""
NLP Module: Skill Extraction using spaCy + keyword matching
Extracts skills, experience, education from raw resume text.
"""
import re
import spacy
from typing import Optional

# Load spaCy model (falls back gracefully if not installed)
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except OSError:
    SPACY_AVAILABLE = False
    print("[NLP] spaCy model not found. Using keyword-only extraction.")

# ─── Master Skills Database ───────────────────────────────────────────────────
SKILLS_DB = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB",
        "Perl", "Haskell", "Lua", "Dart", "Elixir"
    ],
    "Web Frontend": [
        "React", "Vue", "Angular", "Next.js", "Nuxt", "Svelte", "HTML",
        "CSS", "Sass", "Tailwind", "Bootstrap", "jQuery", "Redux",
        "GraphQL", "Webpack", "Vite"
    ],
    "Web Backend": [
        "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
        "Laravel", "Rails", "ASP.NET", "Gin", "Fiber", "NestJS", "Koa",
        "REST API", "Microservices", "gRPC"
    ],
    "Databases": [
        "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Cassandra",
        "Elasticsearch", "DynamoDB", "Oracle", "SQL Server", "Firebase",
        "Supabase", "CouchDB", "InfluxDB"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "GitHub Actions", "CircleCI", "CI/CD",
        "Linux", "Nginx", "Apache", "Cloudflare", "Vercel", "Heroku"
    ],
    "Data & ML": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "NLP", "Computer Vision", "Data Analysis", "Tableau", "Power BI",
        "Apache Spark", "Hadoop", "Airflow", "MLflow", "Hugging Face"
    ],
    "Mobile": [
        "React Native", "Flutter", "iOS", "Android", "Expo",
        "Xamarin", "Ionic", "SwiftUI", "Jetpack Compose"
    ],
    "Tools & Practices": [
        "Git", "GitHub", "GitLab", "Jira", "Confluence", "Figma",
        "Postman", "Swagger", "VS Code", "Agile", "Scrum", "Kanban",
        "TDD", "BDD", "Unit Testing", "Jest", "Pytest", "Selenium"
    ],
    "Soft Skills": [
        "Leadership", "Communication", "Teamwork", "Problem Solving",
        "Project Management", "Critical Thinking", "Time Management",
        "Mentoring", "Public Speaking", "Negotiation"
    ]
}

# Flatten for quick lookup
ALL_SKILLS = {s.lower(): s for cat in SKILLS_DB.values() for s in cat}

# Education keywords
EDUCATION_LEVELS = {
    "phd": "PhD",
    "ph.d": "PhD",
    "doctorate": "PhD",
    "master": "Master's",
    "m.s.": "Master's",
    "m.sc": "Master's",
    "mba": "Master's",
    "bachelor": "Bachelor's",
    "b.s.": "Bachelor's",
    "b.sc": "Bachelor's",
    "b.tech": "Bachelor's",
    "b.e.": "Bachelor's",
    "undergraduate": "Bachelor's",
    "high school": "High School",
    "diploma": "Diploma",
    "associate": "Associate's"
}

# Experience patterns
EXP_PATTERNS = [
    r"(\d+)\+?\s*years?\s+(?:of\s+)?experience",
    r"experience\s+of\s+(\d+)\+?\s*years?",
    r"(\d+)\+?\s*years?\s+(?:of\s+)?(?:work|professional|industry)",
    r"worked\s+for\s+(\d+)\+?\s*years?"
]


def extract_skills(text: str) -> list[str]:
    """Extract skills from resume text using keyword matching + spaCy NER."""
    found = set()
    text_lower = text.lower()

    # Keyword matching
    for skill_lower, skill_original in ALL_SKILLS.items():
        # Use word boundary matching for short skills to avoid false positives
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill_original)

    # spaCy NER boost (extracts ORG/PRODUCT names that might be tech skills)
    if SPACY_AVAILABLE and len(text) < 50000:
        doc = nlp(text[:10000])  # Process first 10k chars
        for ent in doc.ents:
            if ent.label_ in ("ORG", "PRODUCT"):
                ent_lower = ent.text.lower()
                if ent_lower in ALL_SKILLS:
                    found.add(ALL_SKILLS[ent_lower])

    return sorted(list(found))


def extract_experience_years(text: str) -> int:
    """Estimate years of experience from resume text."""
    text_lower = text.lower()
    for pattern in EXP_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))

    # Count job entries as fallback
    job_indicators = len(re.findall(
        r'\b(20\d{2}|19\d{2})\s*[-–]\s*(20\d{2}|present|current)',
        text_lower
    ))
    if job_indicators >= 3:
        return job_indicators * 2
    elif job_indicators == 2:
        return 3
    elif job_indicators == 1:
        return 1
    return 0


def extract_education(text: str) -> str:
    """Detect highest education level from resume text."""
    text_lower = text.lower()
    hierarchy = ["PhD", "Master's", "Bachelor's", "Associate's", "Diploma", "High School"]

    found_levels = set()
    for keyword, level in EDUCATION_LEVELS.items():
        if keyword in text_lower:
            found_levels.add(level)

    for level in hierarchy:
        if level in found_levels:
            return level
    return "Not Specified"


def extract_contact_info(text: str) -> dict:
    """Extract name, email, phone from resume text."""
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone_match = re.search(
        r'(\+?1?\s?)?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})', text
    )

    # Name: try first line that looks like a name (2-4 capitalized words)
    name = "Unknown"
    for line in text.split('\n')[:10]:
        line = line.strip()
        if re.match(r'^[A-Z][a-z]+ ([A-Z][a-z]+ ?){1,3}$', line):
            name = line
            break

    return {
        "name": name,
        "email": email_match.group(0) if email_match else "Not found",
        "phone": phone_match.group(0) if phone_match else "Not found"
    }


def calculate_resume_score(skills: list, exp_years: int, education: str, text: str) -> dict:
    """Calculate resume score with breakdown."""
    # Skills score (max 40)
    skill_score = min(40, len(skills) * 2)

    # Experience score (max 30)
    if exp_years >= 10:
        exp_score = 30
    elif exp_years >= 5:
        exp_score = 24
    elif exp_years >= 3:
        exp_score = 18
    elif exp_years >= 1:
        exp_score = 10
    else:
        exp_score = 4

    # Education score (max 15)
    edu_map = {"PhD": 15, "Master's": 12, "Bachelor's": 10,
               "Associate's": 7, "Diploma": 5, "High School": 3, "Not Specified": 2}
    edu_score = edu_map.get(education, 2)

    # Formatting score (max 15) - heuristic checks
    fmt_score = 0
    text_lower = text.lower()
    if any(w in text_lower for w in ["experience", "work history", "employment"]):
        fmt_score += 3
    if any(w in text_lower for w in ["education", "academic", "degree"]):
        fmt_score += 3
    if any(w in text_lower for w in ["skills", "technical skills", "competencies"]):
        fmt_score += 3
    if any(w in text_lower for w in ["project", "projects", "portfolio"]):
        fmt_score += 3
    if email_present(text):
        fmt_score += 3

    total = skill_score + exp_score + edu_score + fmt_score
    return {
        "resumeScore": min(100, total),
        "scoreBreakdown": {
            "skillsScore": skill_score,
            "experienceScore": exp_score,
            "educationScore": edu_score,
            "formattingScore": fmt_score
        }
    }


def email_present(text: str) -> bool:
    return bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))


def recommend_jobs(skills: list) -> list:
    """Recommend job roles based on detected skills."""
    JOB_ROLES = {
        "Frontend Developer": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "Vue", "Angular"],
        "Backend Developer": ["Python", "Node.js", "Java", "PostgreSQL", "MongoDB", "REST API", "Docker"],
        "Full Stack Developer": ["React", "Node.js", "MongoDB", "JavaScript", "REST API", "Docker", "Git"],
        "Data Scientist": ["Python", "Machine Learning", "Pandas", "NumPy", "TensorFlow", "Data Analysis"],
        "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Docker", "Kubernetes", "NLP", "scikit-learn"],
        "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Linux", "Git", "Terraform"],
        "Cloud Architect": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Microservices"],
        "Mobile Developer": ["React Native", "Flutter", "iOS", "Android", "Swift", "Kotlin"],
        "Data Engineer": ["Python", "Apache Spark", "Hadoop", "SQL", "Airflow", "AWS", "Pandas"],
        "Security Engineer": ["Linux", "Python", "AWS", "Docker", "Git", "Kubernetes"]
    }

    skill_set = set(skills)
    scores = {}
    for role, required in JOB_ROLES.items():
        match = len(skill_set.intersection(set(required)))
        if match > 0:
            scores[role] = match / len(required)

    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [role for role, _ in sorted_roles[:3]]


def get_missing_skills(skills: list, recommended_roles: list) -> list:
    """Return important missing skills based on recommended roles."""
    JOB_ROLES = {
        "Frontend Developer": ["React", "TypeScript", "CSS", "Next.js", "Testing"],
        "Backend Developer": ["Docker", "PostgreSQL", "REST API", "Redis", "CI/CD"],
        "Full Stack Developer": ["Docker", "TypeScript", "Redis", "CI/CD", "Testing"],
        "Data Scientist": ["TensorFlow", "PyTorch", "SQL", "Tableau", "Airflow"],
        "ML Engineer": ["Kubernetes", "MLflow", "Hugging Face", "Apache Spark", "Airflow"],
        "DevOps Engineer": ["Ansible", "Terraform", "Jenkins", "Prometheus", "Grafana"],
        "Cloud Architect": ["Terraform", "Ansible", "Microservices", "Redis", "CI/CD"],
    }

    skill_set = set(skills)
    missing = set()
    for role in recommended_roles:
        if role in JOB_ROLES:
            for s in JOB_ROLES[role]:
                if s not in skill_set:
                    missing.add(s)
    return list(missing)[:6]


def full_analysis(text: str) -> dict:
    """Run full NLP analysis on resume text."""
    contact = extract_contact_info(text)
    skills = extract_skills(text)
    exp_years = extract_experience_years(text)
    education = extract_education(text)
    scores = calculate_resume_score(skills, exp_years, education, text)
    recommended_roles = recommend_jobs(skills)
    missing_skills = get_missing_skills(skills, recommended_roles)

    return {
        **contact,
        "detectedSkills": skills,
        "experienceYears": exp_years,
        "educationLevel": education,
        **scores,
        "recommendedRoles": recommended_roles,
        "missingSkills": missing_skills,
        "summary": f"Candidate with {exp_years} years of experience and {education} education. "
                   f"Detected {len(skills)} relevant technical skills.",
        "strengths": _get_strengths(skills, exp_years, education),
        "improvements": _get_improvements(skills, exp_years, text),
    }


def _get_strengths(skills, exp_years, education):
    strengths = []
    if len(skills) >= 10:
        strengths.append(f"Strong technical breadth with {len(skills)} detected skills")
    elif len(skills) >= 5:
        strengths.append(f"Good technical foundation with {len(skills)} relevant skills")
    if exp_years >= 5:
        strengths.append(f"Experienced professional with {exp_years}+ years in the field")
    if education in ("PhD", "Master's"):
        strengths.append(f"Advanced academic background ({education} degree)")
    if len(strengths) < 3:
        strengths.append("Demonstrates diverse skill set across multiple domains")
    if len(strengths) < 3:
        strengths.append("Shows potential for growth and learning")
    return strengths[:3]


def _get_improvements(skills, exp_years, text):
    improvements = []
    if len(skills) < 5:
        improvements.append("Add more specific technical skills with proficiency levels")
    if exp_years == 0:
        improvements.append("Quantify experience with specific years and dates")
    if "project" not in text.lower():
        improvements.append("Include a Projects section with measurable outcomes")
    if not email_present(text):
        improvements.append("Ensure contact information (email, phone) is clearly listed")
    improvements.append("Use action verbs (built, led, designed, optimized) to describe achievements")
    return improvements[:3]
