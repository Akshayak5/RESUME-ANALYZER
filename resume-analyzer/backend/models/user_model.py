from database.connection import get_db
from bson import ObjectId
from datetime import datetime
import bcrypt


class UserModel:

    @staticmethod
    def collection():
        return get_db().users

    @staticmethod
    def create(name: str, email: str, password: str) -> dict:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = {
            "name": name,
            "email": email.lower().strip(),
            "password": hashed,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "resume_count": 0,
            "verified_skills": [],
            "profile": {
                "bio": "",
                "location": "",
                "linkedin": "",
                "github": ""
            }
        }
        result = UserModel.collection().insert_one(user)
        user["_id"] = str(result.inserted_id)
        user.pop("password", None)
        return user

    @staticmethod
    def find_by_email(email: str) -> dict | None:
        return UserModel.collection().find_one({"email": email.lower().strip()})

    @staticmethod
    def find_by_id(user_id: str) -> dict | None:
        try:
            return UserModel.collection().find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    def verify_password(plain: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)

    @staticmethod
    def add_verified_skill(user_id: str, skill: str):
        UserModel.collection().update_one(
            {"_id": ObjectId(user_id)},
            {
                "$addToSet": {"verified_skills": skill},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

    @staticmethod
    def increment_resume_count(user_id: str):
        UserModel.collection().update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"resume_count": 1}}
        )

    @staticmethod
    def serialize(user: dict) -> dict:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        return user
