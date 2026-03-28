from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.resume_model import ResumeModel
from models.skill_verification_model import SkillVerificationModel
from models.user_model import UserModel

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    resume_stats = ResumeModel.get_stats(user_id)
    verifications = SkillVerificationModel.get_user_verifications(user_id)
    verified_skills = list({v["skill"] for v in verifications})
    user = UserModel.find_by_id(user_id)

    return jsonify({
        "user": UserModel.serialize(user) if user else {},
        "resume_stats": resume_stats,
        "verified_skills": verified_skills,
        "verified_count": len(verified_skills),
        "total_quiz_attempts": len(verifications),
    }), 200


@dashboard_bp.route("/recent-activity", methods=["GET"])
@jwt_required()
def recent_activity():
    user_id = get_jwt_identity()
    resumes = ResumeModel.find_by_user(user_id, limit=5)
    verifications = SkillVerificationModel.get_user_verifications(user_id)

    activity = []
    for r in resumes:
        activity.append({
            "type": "resume_upload",
            "description": f"Analyzed resume: {r.get('filename', 'resume')}",
            "score": r.get("score", 0),
            "timestamp": str(r.get("created_at", ""))
        })
    for v in verifications[:5]:
        activity.append({
            "type": "skill_verified",
            "description": f"Verified skill: {v['skill']}",
            "score": v.get("percentage", 0),
            "timestamp": str(v.get("attempted_at", ""))
        })

    activity.sort(key=lambda x: x["timestamp"], reverse=True)
    return jsonify({"activity": activity[:10]}), 200


@dashboard_bp.route("/progress", methods=["GET"])
@jwt_required()
def get_progress():
    user_id = get_jwt_identity()
    resumes = ResumeModel.find_by_user(user_id)

    if not resumes:
        return jsonify({"progress": [], "improvement": 0}), 200

    progress = [
        {
            "score": r.get("score", 0),
            "date": str(r.get("created_at", "")),
            "filename": r.get("filename", "resume")
        }
        for r in reversed(resumes)
    ]

    improvement = 0
    if len(progress) >= 2:
        improvement = progress[-1]["score"] - progress[0]["score"]

    return jsonify({"progress": progress, "improvement": improvement}), 200
