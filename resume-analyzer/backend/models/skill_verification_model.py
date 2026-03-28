from database.connection import get_db
from bson import ObjectId
from datetime import datetime


class SkillVerificationModel:

    @staticmethod
    def collection():
        return get_db().skill_verifications

    @staticmethod
    def save_attempt(user_id: str, skill: str, score: int, total: int, passed: bool) -> dict:
        doc = {
            "user_id": user_id,
            "skill": skill,
            "score": score,
            "total": total,
            "passed": passed,
            "percentage": round((score / total) * 100, 1) if total else 0,
            "attempted_at": datetime.utcnow()
        }
        result = SkillVerificationModel.collection().insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc

    @staticmethod
    def get_user_verifications(user_id: str) -> list:
        cursor = SkillVerificationModel.collection().find(
            {"user_id": user_id, "passed": True}
        ).sort("attempted_at", -1)
        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    def get_attempts(user_id: str, skill: str) -> list:
        cursor = SkillVerificationModel.collection().find(
            {"user_id": user_id, "skill": skill}
        ).sort("attempted_at", -1)
        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    def is_verified(user_id: str, skill: str) -> bool:
        doc = SkillVerificationModel.collection().find_one(
            {"user_id": user_id, "skill": skill, "passed": True}
        )
        return doc is not None
