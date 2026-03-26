from datetime import datetime, timezone


def resume_schema(user_id, filename, parsed, analysis):
    return {
        "user_id":     user_id,
        "filename":    filename,
        "uploaded_at": datetime.now(timezone.utc),
        "candidate": {
            "name":     parsed.get("name", ""),
            "email":    parsed.get("email", ""),
            "phone":    parsed.get("phone", ""),
            "raw_text": parsed.get("raw_text") or parsed.get("text") or "",  # needed for AI enhance
        },
        "analysis": {
            "skills":           analysis.get("skills", []),
            "categorized":      analysis.get("categorized", {}),
            "score":            analysis.get("score", 0),
            "missing_skills":   analysis.get("missing_skills", []),
            "recommended_jobs": analysis.get("recommended_jobs", []),
            "experience_years": analysis.get("experience_years", 0),
            "verified_skills":  analysis.get("verified_skills", []),
        },
    }


def user_schema(name, email, pwd_hash, role="candidate"):
    return {
        "name":       name,
        "email":      email,
        "password":   pwd_hash,
        "role":       role,
        "created_at": datetime.utcnow(),
    }


def test_result_schema(user_id, skill, score, total):
    return {
        "user_id":  user_id,
        "skill":    skill,
        "score":    score,
        "total":    total,
        "passed":   score / total >= 0.6,
        "taken_at": datetime.now(timezone.utc),
    }