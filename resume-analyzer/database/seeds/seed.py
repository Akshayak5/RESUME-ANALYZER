"""
Seed script: Creates sample data in MongoDB for development/testing.
Run: python database/seeds/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.connection import init_db, get_db
from models.user_model import UserModel
from models.resume_model import ResumeModel
from models.skill_verification_model import SkillVerificationModel
from datetime import datetime

SAMPLE_ANALYSIS = {
    "name": "Alex Johnson",
    "email": "alex@example.com",
    "phone": "+1-555-0101",
    "summary": "Experienced full-stack developer with 4 years in web technologies.",
    "detectedSkills": ["Python", "React", "JavaScript", "Docker", "MongoDB", "SQL", "Git"],
    "experienceYears": 4,
    "educationLevel": "Bachelor's",
    "resumeScore": 72,
    "scoreBreakdown": {"skillsScore": 28, "experienceScore": 20, "educationScore": 10, "formattingScore": 14},
    "strengths": ["Strong JS ecosystem knowledge", "Experience with containerization", "Full-stack capability"],
    "improvements": ["Add cloud certifications", "Include measurable project outcomes", "Add testing frameworks"],
    "missingSkills": ["TypeScript", "Kubernetes", "AWS", "CI/CD", "GraphQL"],
    "recommendedRoles": ["Full Stack Developer", "Backend Developer", "Frontend Developer"]
}


def seed():
    print("[Seed] Initializing database...")
    init_db()
    db = get_db()

    # Clear existing seed data
    db.users.delete_many({"email": {"$in": ["demo@resumeai.dev", "test@resumeai.dev"]}})

    # Create demo user
    print("[Seed] Creating demo user...")
    user = UserModel.create("Demo User", "demo@resumeai.dev", "demo1234")
    user_id = user["_id"]
    print(f"  ✓ Created user: demo@resumeai.dev / demo1234")

    # Create sample resumes
    print("[Seed] Creating sample resumes...")
    for i, score in enumerate([58, 65, 72]):
        analysis = {**SAMPLE_ANALYSIS, "resumeScore": score, "scoreBreakdown": {
            "skillsScore": score // 2, "experienceScore": score // 3,
            "educationScore": 10, "formattingScore": 12
        }}
        ResumeModel.create(user_id, f"resume_v{i+1}.pdf", analysis)
        print(f"  ✓ Created resume v{i+1} (score: {score})")

    # Create skill verifications
    print("[Seed] Creating skill verifications...")
    for skill in ["Python", "React", "Docker"]:
        SkillVerificationModel.save_attempt(user_id, skill, 3, 4, True)
        UserModel.add_verified_skill(user_id, skill)
        print(f"  ✓ Verified skill: {skill}")

    UserModel.increment_resume_count(user_id)
    UserModel.increment_resume_count(user_id)
    UserModel.increment_resume_count(user_id)

    print("\n[Seed] ✅ Database seeded successfully!")
    print("  Demo login: demo@resumeai.dev / demo1234")


if __name__ == "__main__":
    seed()
