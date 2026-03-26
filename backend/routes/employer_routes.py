from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
import traceback

employer_bp = Blueprint("employer", __name__)


def get_db():
    if hasattr(current_app._get_current_object(), 'mongo'):
        return current_app._get_current_object().mongo.db
    from backend.app import mongo
    return mongo.db


@employer_bp.route("/candidates", methods=["GET"])
def candidates():
    try:
        db = get_db()

        # Query params for filtering
        min_score  = int(request.args.get("min_score", 0))
        min_exp    = int(request.args.get("min_exp", 0))
        skills     = request.args.get("skills", "")        # comma-separated
        verified   = request.args.get("verified_only", "false").lower() == "true"
        search     = request.args.get("search", "").strip()

        # Build MongoDB query
        query = {}

        if min_score > 0:
            query["analysis.score"] = {"$gte": min_score}

        if min_exp > 0:
            query["analysis.experience_years"] = {"$gte": min_exp}

        if skills:
            skill_list = [s.strip() for s in skills.split(",") if s.strip()]
            if skill_list:
                query["analysis.skills"] = {"$all": skill_list}

        if verified:
            query["analysis.verified_skills"] = {"$exists": True, "$ne": []}

        if search:
            query["$or"] = [
                {"candidate.name":  {"$regex": search, "$options": "i"}},
                {"candidate.email": {"$regex": search, "$options": "i"}},
                {"analysis.skills": {"$regex": search, "$options": "i"}},
            ]

        docs = list(
            db.resumes.find(
                query,
                {
                    "_id": 1,
                    "filename": 1,
                    "uploaded_at": 1,
                    "candidate.name": 1,
                    "candidate.email": 1,
                    "candidate.phone": 1,
                    "analysis.score": 1,
                    "analysis.skills": 1,
                    "analysis.experience_years": 1,
                    "analysis.verified_skills": 1,
                    "analysis.recommended_jobs": 1,
                }
            )
            .sort("analysis.score", -1)
            .limit(100)
        )

        results = []
        for d in docs:
            score = d.get("analysis", {}).get("score", 0)
            try:
                score = int(score)
            except (TypeError, ValueError):
                score = 0

            uploaded_at = d.get("uploaded_at")
            results.append({
                "_id":              str(d["_id"]),
                "filename":         d.get("filename", ""),
                "uploaded_at":      uploaded_at.isoformat() if uploaded_at else "",
                "candidate":        d.get("candidate", {}),
                "score":            score,
                "skills":           d.get("analysis", {}).get("skills", []),
                "experience_years": d.get("analysis", {}).get("experience_years", 0),
                "verified_skills":  d.get("analysis", {}).get("verified_skills", []),
                "recommended_jobs": d.get("analysis", {}).get("recommended_jobs", []),
            })

        return jsonify({"candidates": results, "total": len(results)}), 200

    except Exception as e:
        current_app.logger.error(f"candidates error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500