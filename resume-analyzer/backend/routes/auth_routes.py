from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user_model import UserModel
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not all([name, email, password]):
        return jsonify({"error": "Name, email and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if UserModel.find_by_email(email):
        return jsonify({"error": "Email already registered"}), 409

    user = UserModel.create(name, email, password)
    token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(days=7))
    return jsonify({"message": "Account created", "token": token, "user": user}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not all([email, password]):
        return jsonify({"error": "Email and password required"}), 400

    user = UserModel.find_by_email(email)
    if not user or not UserModel.verify_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(days=7))
    return jsonify({"message": "Login successful", "token": token, "user": UserModel.serialize(user)}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = UserModel.find_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserModel.serialize(user)), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    allowed = ["name", "profile"]
    update = {k: v for k, v in data.items() if k in allowed}
    if not update:
        return jsonify({"error": "No valid fields provided"}), 400
    from database.connection import get_db
    from bson import ObjectId
    from datetime import datetime
    get_db().users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {**update, "updated_at": datetime.utcnow()}}
    )
    user = UserModel.find_by_id(user_id)
    return jsonify(UserModel.serialize(user)), 200
