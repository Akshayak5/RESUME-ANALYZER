
from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/resumeiq")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

# Single PyMongo instance — stored on app so routes can access it
mongo = PyMongo(app)
app.mongo = mongo   # ← attach to app so get_db() in routes works reliably

# Register blueprints — static routes inside each blueprint must come before /<id>
from backend.routes.resume_routes   import resume_bp
from backend.routes.auth_routes     import auth_bp
from backend.routes.employer_routes import employer_bp

app.register_blueprint(resume_bp,   url_prefix="/api/resume")
app.register_blueprint(auth_bp,     url_prefix="/api/auth")
app.register_blueprint(employer_bp, url_prefix="/api/employer")


# ── Frontend pages ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/employer")
def employer():
    return render_template("employer.html")


# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    from flask import jsonify
    try:
        app.mongo.db.command("ping")
        return jsonify({"status": "ok", "mongo": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "mongo": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )