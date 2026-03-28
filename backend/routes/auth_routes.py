from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import traceback
import re
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# Strong password regex: min 8 chars, at least one letter, one number, one special char
STRONG_PWD = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$')


def get_db():
    if hasattr(current_app._get_current_object(), 'mongo'):
        return current_app._get_current_object().mongo.db
    from backend.app import mongo
    return mongo.db


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}
        name     = (data.get("name") or "").strip()
        email    = (data.get("email") or "").strip().lower()
        password = (data.get("password") or "").strip()
        role     = (data.get("role") or "candidate").strip()

        if not name or not email or not password:
            return jsonify({"error": "Name, email and password are required"}), 400

        if not STRONG_PWD.match(password):
            return jsonify({
                "error": "Password must be at least 8 characters with a letter, number, and special character (@$!%*#?&)"
            }), 400

        if role not in ("candidate", "employer"):
            return jsonify({"error": "Role must be candidate or employer"}), 400

        db = get_db()
        if db.users.find_one({"email": email}):
            return jsonify({"error": "Email already registered"}), 409

        user = {
            "name":       name,
            "email":      email,
            "password":   generate_password_hash(password),
            "role":       role,
            "created_at": datetime.utcnow(),
        }
        uid = str(db.users.insert_one(user).inserted_id)

        return jsonify({
            "user_id": uid,
            "name":    name,
            "email":   email,
            "role":    role,
        }), 201

    except Exception as e:
        current_app.logger.error(f"register error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data     = request.get_json() or {}
        email    = (data.get("email") or "").strip().lower()
        password = (data.get("password") or "").strip()

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        db   = get_db()
        user = db.users.find_one({"email": email})

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({
            "user_id": str(user["_id"]),
            "name":    user["name"],
            "email":   user["email"],
            "role":    user.get("role", "candidate"),
        }), 200

    except Exception as e:
        current_app.logger.error(f"login error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/profile/<user_id>", methods=["GET"])
def profile(user_id):
    try:
        db   = get_db()
        user = db.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404
        user["_id"] = str(user["_id"])
        return jsonify(user), 200

    except Exception as e:
        current_app.logger.error(f"profile error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data         = request.get_json() or {}
        email        = (data.get("email") or "").strip().lower()
        new_password = (data.get("new_password") or "").strip()

        if not email or not new_password:
            return jsonify({"error": "Email and new password are required"}), 400

        if not STRONG_PWD.match(new_password):
            return jsonify({
                "error": "Password must be at least 8 characters with a letter, number, and special character (@$!%*#?&)"
            }), 400

        db   = get_db()
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"error": "No account found with that email"}), 404

        db.users.update_one(
            {"email": email},
            {"$set": {"password": generate_password_hash(new_password)}}
        )

        return jsonify({"success": True, "message": "Password reset successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"reset-password error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500