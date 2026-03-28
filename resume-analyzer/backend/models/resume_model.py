from database.connection import get_db
from bson import ObjectId
from datetime import datetime


class ResumeModel:

    @staticmethod
    def collection():
        return get_db().resumes

    @staticmethod
    def create(user_id: str, filename: str, analysis: dict) -> dict:
        doc = {
            "user_id": user_id,
            "filename": filename,
            "created_at": datetime.utcnow(),
            "analysis": analysis,
            "score": analysis.get("resumeScore", 0),
            "detected_skills": analysis.get("detectedSkills", []),
            "recommended_roles": analysis.get("recommendedRoles", []),
        }
        result = ResumeModel.collection().insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc

    @staticmethod
    def find_by_user(user_id: str, limit: int = 20) -> list:
        cursor = ResumeModel.collection().find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit)
        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    def find_by_id(resume_id: str) -> dict | None:
        try:
            doc = ResumeModel.collection().find_one({"_id": ObjectId(resume_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception:
            return None

    @staticmethod
    def delete(resume_id: str, user_id: str) -> bool:
        result = ResumeModel.collection().delete_one(
            {"_id": ObjectId(resume_id), "user_id": user_id}
        )
        return result.deleted_count > 0

    @staticmethod
    def get_stats(user_id: str) -> dict:
        resumes = ResumeModel.find_by_user(user_id)
        if not resumes:
            return {"total": 0, "avg_score": 0, "best_score": 0, "all_skills": []}
        scores = [r.get("score", 0) for r in resumes]
        all_skills = []
        for r in resumes:
            all_skills.extend(r.get("detected_skills", []))
        return {
            "total": len(resumes),
            "avg_score": round(sum(scores) / len(scores), 1),
            "best_score": max(scores),
            "all_skills": list(set(all_skills))
        }
