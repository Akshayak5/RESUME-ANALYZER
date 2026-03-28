from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from database.connection import init_db
from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.quiz_routes import quiz_bp
from routes.dashboard_routes import dashboard_bp

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:5500"])

# Config
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")

# Create uploads dir
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# JWT
jwt = JWTManager(app)

# Init DB
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(resume_bp, url_prefix="/api/resume")
app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")


@app.route("/api/health")
def health():
    return {"status": "ok", "message": "ResumeAI API is running"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
