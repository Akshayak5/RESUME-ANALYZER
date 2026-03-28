from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid

from models.resume_model import ResumeModel
from models.user_model import UserModel
from utils.parser import parse_resume, is_allowed_file
from nlp.extractor import full_analysis

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not is_allowed_file(file.filename):
        return jsonify({"error": "File type not supported. Use PDF, DOCX, or TXT"}), 400

    # Save file with unique name
    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(filepath)

    try:
        # Parse text
        text = parse_resume(filepath)
        if not text or len(text.strip()) < 50:
            os.remove(filepath)
            return jsonify({"error": "Could not extract text from file. Please try a different format."}), 422

        # Run NLP analysis
        analysis = full_analysis(text)

        # Save to DB
        resume = ResumeModel.create(user_id, secure_filename(file.filename), analysis)
        UserModel.increment_resume_count(user_id)

        # Clean up file
        os.remove(filepath)

        return jsonify({"message": "Resume analyzed successfully", "resume": resume}), 201

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": str(e)}), 500


@resume_bp.route("/analyze-text", methods=["POST"])
@jwt_required()
def analyze_text():
    """Analyze raw pasted resume text."""
    user_id = get_jwt_identity()
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text or len(text) < 50:
        return jsonify({"error": "Resume text too short (minimum 50 characters)"}), 400

    try:
        analysis = full_analysis(text)
        resume = ResumeModel.create(user_id, "pasted_resume.txt", analysis)
        UserModel.increment_resume_count(user_id)
        return jsonify({"message": "Resume analyzed successfully", "resume": resume}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@resume_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    limit = request.args.get("limit", 20, type=int)
    resumes = ResumeModel.find_by_user(user_id, limit)
    return jsonify({"resumes": resumes, "total": len(resumes)}), 200


@resume_bp.route("/<resume_id>", methods=["GET"])
@jwt_required()
def get_resume(resume_id):
    user_id = get_jwt_identity()
    resume = ResumeModel.find_by_id(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404
    if resume["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(resume), 200


@resume_bp.route("/<resume_id>", methods=["DELETE"])
@jwt_required()
def delete_resume(resume_id):
    user_id = get_jwt_identity()
    deleted = ResumeModel.delete(resume_id, user_id)
    if not deleted:
        return jsonify({"error": "Resume not found or unauthorized"}), 404
    return jsonify({"message": "Resume deleted"}), 200
