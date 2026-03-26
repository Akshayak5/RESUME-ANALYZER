import re
import datetime

SKILL_DB = {
    # ── Technology ─────────────────────────────────────────────────────────────
    "Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "R",
        "Swift", "Kotlin", "Rust", "PHP", "Ruby", "Scala", "MATLAB", "Bash",
        "PowerShell", "SQL", "HTML", "CSS",
    ],
    "Web Frameworks": [
        "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI",
        "Spring", "Spring Boot", "Express", "Next.js", "Nuxt.js", "Laravel",
        "ASP.NET", "Rails",
    ],
    "Databases": [
        "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch", "SQLite",
        "Cassandra", "DynamoDB", "Oracle", "Firebase", "MariaDB", "MS SQL",
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Terraform",
        "Ansible", "Jenkins", "GitHub Actions", "Helm", "Linux", "Nginx",
        "GitLab CI", "CircleCI",
    ],
    "AI & ML": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP",
        "Scikit-learn", "Pandas", "NumPy", "Keras", "OpenCV", "Computer Vision",
        "LangChain", "Hugging Face",
    ],
    "Dev Tools": [
        "Git", "REST API", "GraphQL", "Postman", "Jira", "Confluence", "Figma",
        "VS Code", "GitHub", "GitLab", "Bitbucket", "Webpack", "Vite",
        "Microservices", "System Design", "OOP", "Agile", "Scrum", "DevOps",
    ],

    # ── Law Enforcement & Security ─────────────────────────────────────────────
    "Law Enforcement": [
        "MLEO", "MLEO Parking Enforcement", "By-law Enforcement", "By-law Compliance",
        "Regulatory Compliance", "Occurrence Report Writing", "Report Writing",
        "Progressive Enforcement", "Enforcement Patrol", "Site Patrol",
        "Complaint Investigation", "Complaint Intake", "Evidence Handling",
        "Evidence Continuity", "Use of Force", "Nonviolent Crisis Intervention",
        "CPI", "Conflict De-escalation", "De-escalation",
        "Police Coordination", "Interagency Coordination", "Emergency Response",
        "Naloxone Administration", "Naloxone", "Public Safety",
        "Traffic Control", "Crowd Control", "Security Guard",
        "Asset Protection", "Loss Prevention", "Theft Investigation",
        "Safety Monitoring", "Patrol", "Surveillance",
        "Incident Documentation", "Legally Defensible Documentation",
        "Law Enforcement", "Municipal Enforcement",
    ],

    # ── Healthcare & Medical ───────────────────────────────────────────────────
    "Healthcare": [
        "Clinical Research", "Patient Care", "Medical Coding", "ICD-10", "CPT Coding",
        "EMR", "EHR", "Epic", "Cerner", "Pharmacology", "Anatomy", "Physiology",
        "Pathology", "Medical Terminology", "HIPAA", "Healthcare Administration",
        "Nursing", "Radiology", "Phlebotomy", "Diagnostics",
        "Public Health", "Epidemiology", "Biostatistics", "Clinical Trials",
        "FDA Regulations", "Pharmacy", "Drug Dispensing", "Pediatrics",
        "Geriatrics", "Psychiatry", "Nutrition", "First Aid", "CPR",
        "BLS", "AED", "Medical Writing", "Lab Techniques", "PCR", "ELISA",
        "Standard First Aid", "Naloxone", "WHMIS",
    ],

    # ── Business & Management ──────────────────────────────────────────────────
    "Business": [
        "Project Management", "PMP", "Risk Management", "Business Analysis",
        "Requirements Gathering", "Process Improvement", "Lean", "Six Sigma",
        "Financial Analysis", "Accounting", "Budgeting", "Forecasting",
        "SAP", "QuickBooks", "Digital Marketing", "SEO", "SEM", "Google Ads",
        "Social Media Marketing", "CRM", "Salesforce", "Sales", "B2B",
        "Negotiation", "Client Relations", "Supply Chain", "Logistics",
        "Procurement", "Inventory Management", "Contract Management",
        "Compliance", "HR Management", "Recruitment", "Talent Acquisition",
        "Onboarding", "Payroll", "SHRM", "Team Leadership", "Team Management",
        "Regulatory Compliance", "Policy Compliance",
    ],

    # ── Design & Creative ──────────────────────────────────────────────────────
    "Design": [
        "UI Design", "UX Design", "Figma", "Adobe XD", "Sketch", "InVision",
        "Wireframing", "Prototyping", "Photoshop", "Illustrator", "InDesign",
        "After Effects", "Premiere Pro", "Graphic Design", "Branding",
        "Typography", "Motion Graphics", "User Research", "Usability Testing",
        "A/B Testing", "Design Systems", "3D Modeling", "Blender",
        "AutoCAD", "SolidWorks", "Revit", "Video Editing", "Animation",
    ],

    # ── Engineering ────────────────────────────────────────────────────────────
    "Engineering": [
        "Mechanical Engineering", "Civil Engineering", "Electrical Engineering",
        "Structural Engineering", "AutoCAD", "MATLAB", "ANSYS", "CATIA",
        "BIM", "Circuit Design", "PCB Layout", "Embedded Systems",
        "PLC Programming", "SCADA", "Thermodynamics", "Fluid Mechanics",
        "Finite Element Analysis", "CAD", "CAM", "Construction Management",
        "Site Supervision", "Quality Control", "NDT", "HVAC",
        "Geotechnical", "Environmental Engineering", "Robotics", "Automation",
        "IoT", "Control Systems",
    ],

    # ── Education ──────────────────────────────────────────────────────────────
    "Education": [
        "Curriculum Development", "Lesson Planning", "Classroom Management",
        "Student Assessment", "E-Learning", "LMS", "Instructional Design",
        "Training and Development", "SCORM", "Special Education",
        "Child Development", "Early Childhood Education", "Academic Research",
        "Grant Writing", "STEM Teaching", "English Teaching", "ESL", "TESOL",
        "Counseling", "Career Guidance", "Online Teaching", "Google Classroom",
        "Canvas", "Blackboard", "Tutoring",
    ],

    # ── Emergency & Community Services ────────────────────────────────────────
    "Community & Emergency Services": [
        "Emergency Management", "Disaster Response", "Evacuation",
        "Community Engagement", "Volunteer Management", "Social Services",
        "Outreach", "Public Education", "Wellness Support",
        "Crisis Intervention", "Safety Awareness", "Multilingual",
        "Cultural Competency", "Community Relations",
        "APCO", "Basic Emergency Management", "Public Safety Telecommunicator",
        "Smart Serve",
    ],

    # ── Certifications (standalone) ────────────────────────────────────────────
    "Certifications": [
        "PMP", "CISSP", "CPA", "CFA", "AWS Certified", "Google Cloud Certified",
        "Scrum Master", "ITIL", "Six Sigma", "WHMIS", "Smart Serve",
        "Ontario Security Guard Licence", "Security Guard Licence",
        "G Class Drivers Licence", "Drivers Licence",
        "Standard First Aid", "CPR", "AED", "Naloxone",
        "Use of Force", "CPI", "APCO", "MLEO",
    ],

    # ── Soft Skills ────────────────────────────────────────────────────────────
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Adaptability", "Attention to Detail",
        "Customer Service", "Multitasking", "Decision Making",
        "Conflict Resolution", "Report Writing", "Documentation",
        "Public Speaking", "Research", "Analytical Skills",
    ],
}

# Build lookup: normalised_lower → (canonical_name, category)
ALL_SKILLS: dict = {}
for _cat, _skills in SKILL_DB.items():
    for _s in _skills:
        ALL_SKILLS[_s.lower()] = (_s, _cat)

PREMIUM_SKILLS = {
    # Tech
    "Docker", "AWS", "Machine Learning", "React", "Python", "Kubernetes",
    "TypeScript", "GCP", "Azure", "PyTorch", "TensorFlow", "Terraform",
    "System Design", "Microservices", "Deep Learning", "FastAPI", "Next.js",
    # Law enforcement
    "MLEO", "MLEO Parking Enforcement", "Use of Force", "Evidence Handling",
    "Conflict De-escalation", "CPI", "Emergency Response", "Asset Protection",
    "Loss Prevention", "Legally Defensible Documentation",
    # Healthcare
    "Standard First Aid", "CPR", "Naloxone", "WHMIS", "Clinical Research",
    # Business
    "Project Management", "PMP", "Six Sigma", "Risk Management",
    # Certifications
    "Ontario Security Guard Licence", "Security Guard Licence",
}

JOB_ROLES = {
    # Tech
    "Python Developer":     {"s": ["Python", "Django", "Flask", "REST API", "Git"],                         "i": "🐍"},
    "Data Analyst":         {"s": ["Python", "SQL", "Machine Learning", "Pandas", "NumPy"],                 "i": "📊"},
    "ML Engineer":          {"s": ["Machine Learning", "TensorFlow", "Python", "PyTorch", "Scikit-learn"],  "i": "🤖"},
    "Full Stack Developer": {"s": ["JavaScript", "React", "Node.js", "MongoDB", "REST API"],                "i": "💻"},
    "DevOps Engineer":      {"s": ["Docker", "Kubernetes", "AWS", "CI/CD", "Terraform"],                    "i": "⚙️"},
    "Backend Developer":    {"s": ["Python", "Java", "REST API", "PostgreSQL", "Docker"],                   "i": "🔧"},
    "Frontend Developer":   {"s": ["JavaScript", "React", "HTML", "CSS", "TypeScript"],                     "i": "🎨"},
    # Law enforcement / security
    "Security Officer":     {"s": ["Security Guard", "Patrol", "Incident Documentation",
                                    "Conflict De-escalation", "Report Writing"],                             "i": "🛡️"},
    "By-law Enforcement Officer": {"s": ["MLEO", "By-law Enforcement", "Regulatory Compliance",
                                          "Occurrence Report Writing", "Progressive Enforcement"],           "i": "⚖️"},
    "Loss Prevention Officer": {"s": ["Asset Protection", "Loss Prevention", "Theft Investigation",
                                       "Evidence Handling", "Surveillance"],                                 "i": "🔍"},
    "Emergency Services":   {"s": ["Emergency Response", "First Aid", "CPR",
                                    "Naloxone", "Crisis Intervention"],                                      "i": "🚨"},
    # Healthcare
    "Healthcare Professional": {"s": ["Patient Care", "First Aid", "CPR", "Medical Terminology",
                                       "Clinical Research"],                                                 "i": "🏥"},
    # Business
    "Project Manager":      {"s": ["Project Management", "Agile", "Scrum", "Risk Management",
                                    "Team Leadership"],                                                      "i": "📋"},
    "Business Analyst":     {"s": ["Business Analysis", "Requirements Gathering",
                                    "Process Improvement", "Agile", "Jira"],                                 "i": "📈"},
}


# ── Skill Extraction ───────────────────────────────────────────────────────────
def _iter_ngrams(text: str):
    """
    Yield all unique 1-, 2-, and 3-grams from text (lowercase).
    Splits on whitespace and most punctuation but keeps dots (Vue.js etc).
    """
    tokens = re.split(r'[\s,;:()\[\]{}<>"\'/\\|•–—]+', text)
    tokens = [t.strip('.-').lower() for t in tokens if t.strip()]

    seen: set = set()
    n = len(tokens)
    for i in range(n):
        for size in (1, 2, 3):
            if i + size > n:
                break
            ng = " ".join(tokens[i: i + size])
            if ng and ng not in seen:
                seen.add(ng)
                yield ng


def extract_skills(text: str) -> dict:
    """
    Scan resume text for known skills using n-gram matching.
    Case-insensitive. Handles multi-word skills like 'Machine Learning',
    'MLEO Parking Enforcement', 'Conflict De-escalation', etc.
    """
    found: set = set()
    categorized: dict = {}

    for ng in _iter_ngrams(text):
        if ng in ALL_SKILLS:
            skill, category = ALL_SKILLS[ng]
            if skill not in found:
                found.add(skill)
                categorized.setdefault(category, []).append(skill)

    # Extra pass: skills with special characters that n-gram split may miss
    special_skills = {
        "C++": "Languages", "C#": "Languages", ".NET": "Web Frameworks",
        "Vue.js": "Web Frameworks", "Node.js": "Web Frameworks",
        "Next.js": "Web Frameworks", "Nuxt.js": "Web Frameworks",
        "Scikit-learn": "AI & ML", "GitHub Actions": "Cloud & DevOps",
        "CI/CD": "Cloud & DevOps", "REST API": "Dev Tools",
        "MS SQL": "Databases", "Spring Boot": "Web Frameworks",
        "ASP.NET": "Web Frameworks", "GitLab CI": "Cloud & DevOps",
        "A/B Testing": "Design", "CPR/AED": "Healthcare",
        "BLS/CPR": "Healthcare", "CPI": "Law Enforcement",
        "MLEO": "Law Enforcement", "WHMIS": "Certifications",
        "Smart Serve": "Community & Emergency Services",
        "De-escalation": "Law Enforcement",
        "Conflict De-escalation": "Law Enforcement",
    }
    text_lower = text.lower()
    for skill, cat in special_skills.items():
        if skill.lower() in text_lower and skill not in found:
            found.add(skill)
            categorized.setdefault(cat, []).append(skill)

    # ── Remove false positives ─────────────────────────────────────────────────────────────────────────────
    # "Express" is a web framework but also appears in "Thai Express" etc.
    # Only keep it if it appears in a clearly technical context.
    false_positive_rules = {
        "Express": [r'express\.?js', r'node.*express', r'express.*framework',
                    r'express.*server', r'express.*api', r'express.*route'],
    }
    to_remove = set()
    for skill, patterns in false_positive_rules.items():
        if skill in found:
            if not any(re.search(p, text, re.I) for p in patterns):
                to_remove.add(skill)
    for skill in to_remove:
        found.discard(skill)
        for cat in list(categorized.keys()):
            if skill in categorized[cat]:
                categorized[cat].remove(skill)
    categorized = {k: v for k, v in categorized.items() if v}

    return {"skills": list(found), "categorized": categorized}


# ── Scoring ────────────────────────────────────────────────────────────────────
def compute_score(skills: list, exp: int = 0) -> int:
    """
    Realistic scoring:
    - Base: starts at 30
    - Hard/technical skills weighted much more than soft skills
    - Soft-skills-only resume cannot exceed 55
    - Freshers (0 exp) cannot exceed 75 even with many skills
    - Experience adds meaningful points for mid/senior level
    """
    if not skills:
        return max(10, min(exp * 4, 25))

    SOFT_SKILL_SET = {s.lower() for s in SKILL_DB.get("Soft Skills", [])}

    hard_skills = [s for s in skills if s.lower() not in SOFT_SKILL_SET]
    soft_skills = [s for s in skills if s.lower() in SOFT_SKILL_SET]

    # No hard skills at all -> cap at 55
    if not hard_skills:
        base = 30 + len(soft_skills) * 3 + min(exp * 2, 10)
        return max(10, min(base, 55))

    # Hard skill score with diminishing returns
    hard_score = 0
    for i, _ in enumerate(hard_skills):
        if i < 3:
            hard_score += 10
        elif i < 7:
            hard_score += 6
        elif i < 12:
            hard_score += 3
        else:
            hard_score += 1

    # Soft skill bonus (small)
    soft_score = min(len(soft_skills) * 2, 10)

    # Category diversity bonus (hard skills only)
    categories = len({ALL_SKILLS.get(s.lower(), (s, "Other"))[1] for s in hard_skills})
    diversity_score = min(categories * 4, 15)

    # Premium skills bonus
    premium_count = sum(1 for s in hard_skills if s in PREMIUM_SKILLS)
    premium_score = min(premium_count * 4, 18)

    # Experience score
    if exp == 0:
        exp_score = 0
    elif exp <= 2:
        exp_score = exp * 4
    elif exp <= 5:
        exp_score = 8 + (exp - 2) * 3
    else:
        exp_score = min(17 + (exp - 5) * 1, 22)

    base = 30
    total = base + hard_score + soft_score + diversity_score + premium_score + exp_score

    # Freshers capped at 75
    if exp == 0:
        total = min(total, 75)

    return max(10, min(int(total), 98))


# ── Job Recommendations ────────────────────────────────────────────────────────
def recommend_jobs(skills: list) -> list:
    skill_set = {s.lower() for s in skills}
    out = []
    for role, meta in JOB_ROLES.items():
        matched = [s for s in meta["s"] if s.lower() in skill_set]
        pct     = round(len(matched) / len(meta["s"]) * 100)
        if pct > 15:
            out.append({
                "title":          role,
                "icon":           meta["i"],
                "match_percent":  pct,
                "matched_skills": matched,
            })
    return sorted(out, key=lambda x: -x["match_percent"])[:6]


# ── Missing Skills ─────────────────────────────────────────────────────────────
def get_missing_skills(skills: list) -> list:
    """
    Returns top missing skills — domain-aware.
    Detects if the resume is tech or non-tech and adjusts suggestions.
    """
    tech_skills = {"Python", "JavaScript", "Docker", "AWS", "SQL",
                   "Machine Learning", "Kubernetes", "TypeScript", "React", "Git"}
    enforcement_skills = {"Report Writing", "Conflict De-escalation", "Evidence Handling",
                           "Emergency Response", "First Aid", "CPR", "Regulatory Compliance",
                           "Patrol", "Community Engagement", "Risk Management"}

    skill_set = {s.lower() for s in skills}
    is_enforcement = any(k in skill_set for k in {
        "mleo", "security guard", "by-law enforcement", "patrol",
        "loss prevention", "asset protection", "enforcement patrol"
    })

    if is_enforcement:
        candidates = [
            "Report Writing", "Conflict De-escalation", "Evidence Handling",
            "Emergency Response", "First Aid", "CPR", "WHMIS",
            "Regulatory Compliance", "Risk Management", "Community Engagement",
            "Crisis Intervention", "Team Leadership", "Documentation",
            "Police Coordination", "Safety Monitoring",
        ]
    else:
        candidates = [
            "Python", "JavaScript", "Docker", "AWS", "SQL",
            "Machine Learning", "Kubernetes", "TypeScript", "React", "Git",
            "PostgreSQL", "MongoDB", "CI/CD", "REST API", "Linux",
            "System Design", "Microservices", "Terraform", "Node.js", "Agile",
        ]

    return [s for s in candidates if s.lower() not in skill_set][:10]


# ── Experience Extraction ──────────────────────────────────────────────────────
def extract_experience_years(text: str) -> int:
    """
    Multi-strategy experience extraction.
    1. Fresher/student detection — returns 0 immediately
    2. Explicit statement: "5 years of experience"
    3. Date ranges inside work section ONLY (never education)
    """
    # Strategy 0 — detect freshers / students explicitly
    fresher_patterns = [
        r'\b(fresher|fresh\s*graduate|recent\s*graduate|entry[\s-]*level)\b',
        r'\b(currently\s*(pursuing|studying|enrolled)|ongoing)\b',
        r'\b(b\.?tech|b\.?e\.?|bca|mca|m\.?tech|b\.?sc|m\.?sc|bachelor|master)\b'
        r'.*\b(pursuing|ongoing|present|current)\b',
        r'graduation\s*year\s*:\s*20(2[4-9]|3\d)',   # Graduating 2024 onwards
    ]
    for pat in fresher_patterns:
        if re.search(pat, text, re.I):
            # Still check for an explicit years claim to allow internships
            m = re.search(
                r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:professional\s*|work\s*|industry\s*|total\s*)?'
                r'(?:experience|exp\.?)',
                text, re.I
            )
            if m and int(m.group(1)) >= 1:
                return min(int(m.group(1)), 30)
            return 0

    # Strategy 1 — explicit statement
    m = re.search(
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:professional\s*|work\s*|industry\s*|total\s*)?'
        r'(?:experience|exp\.?)',
        text, re.I
    )
    if m:
        return min(int(m.group(1)), 30)

    # Strategy 2 — work section date ranges ONLY (strips education dates)
    work_text = _extract_work_section(text)
    if work_text:
        # Remove any lines that look like education (degree keywords)
        edu_line_re = re.compile(
            r'.*(b\.?tech|b\.?e\.?|bca|mca|m\.?tech|b\.?sc|m\.?sc|bachelor|master|'
            r'university|college|school|institute|cgpa|gpa|grade|class\s*x+|sslc|hsc|cbse|icse).*',
            re.I
        )
        cleaned_work = "\n".join(
            line for line in work_text.split("\n")
            if not edu_line_re.match(line.strip())
        )
        years = _sum_date_ranges(cleaned_work)
        if years > 0:
            return years

    # Strategy 3 — No reliable data found → 0 (don't guess from education dates)
    return 0


def _sum_date_ranges(text: str) -> int:
    current = datetime.datetime.now().year
    ranges = re.findall(
        r'((?:19|20)\d{2})\s*[-–—to]+\s*((?:19|20)\d{2}|present|current|now|till\s*date|today)',
        text, re.I
    )
    total = 0
    seen: set = set()
    for s_str, e_str in ranges:
        start = int(s_str)
        end   = (current if re.match(r'present|current|now|till\s*date|today', e_str, re.I)
                 else int(e_str))
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        diff = end - start
        if 0 < diff <= 10:
            total += diff
    return min(total, 30)


def _extract_work_section(text: str) -> str:
    work_starts = [
        r'work\s*experience', r'professional\s*experience', r'employment\s*history',
        r'work\s*history',    r'career\s*history',           r'experience',
        r'internship[s]?',    r'professional\s*background',
    ]
    section_ends = [
        r'education', r'academic', r'qualification[s]?', r'skills?',
        r'project[s]?', r'achievement[s]?', r'certification[s]?', r'award[s]?',
        r'publication[s]?', r'reference[s]?', r'language[s]?', r'hobbies?',
        r'interest[s]?', r'volunteer', r'extracurricular', r'community',
    ]
    start_pattern = re.compile(
        r'(?:^|\n)\s*(?:' + '|'.join(work_starts) + r')\s*[:\n]', re.I
    )
    end_pattern = re.compile(
        r'(?:^|\n)\s*(?:' + '|'.join(section_ends) + r')\s*[:\n]', re.I
    )
    m = start_pattern.search(text)
    if not m:
        return ""
    rest  = text[m.end():]
    end_m = end_pattern.search(rest)
    return rest[: end_m.start()] if end_m else rest

# ── Verifiable Skills (Bug 2 fix) ──────────────────────────────────────────────
# Soft skills and certifications cannot be objectively tested in a quiz
_NON_VERIFIABLE_CATEGORIES = {"Soft Skills", "Certifications"}
_NON_VERIFIABLE_SKILLS = {
    # Pure soft skills
    "Communication", "Leadership", "Teamwork", "Problem Solving",
    "Critical Thinking", "Time Management", "Adaptability",
    "Attention to Detail", "Customer Service", "Multitasking",
    "Decision Making", "Conflict Resolution", "Public Speaking",
    "Research", "Analytical Skills",
    # Certifications (you either have the cert or not — not quiz-testable)
    "PMP", "CISSP", "CPA", "CFA", "AWS Certified", "Google Cloud Certified",
    "Scrum Master", "ITIL", "Six Sigma", "WHMIS", "Smart Serve",
    "Ontario Security Guard Licence", "Security Guard Licence",
    "G Class Drivers Licence", "Drivers Licence",
    "Standard First Aid", "CPR", "AED", "Naloxone",
    "Use of Force", "CPI", "APCO", "MLEO",
}


def get_verifiable_skills(skills: list) -> list:
    """
    Returns only skills that can be meaningfully tested with a quiz.
    Filters out pure soft skills and certifications.
    """
    result = []
    for skill in skills:
        category = ALL_SKILLS.get(skill.lower(), (skill, "Other"))[1]
        if category in _NON_VERIFIABLE_CATEGORIES:
            continue
        if skill in _NON_VERIFIABLE_SKILLS:
            continue
        result.append(skill)
    return result