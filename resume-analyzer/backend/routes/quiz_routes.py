from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.skill_verification_model import SkillVerificationModel
from models.user_model import UserModel

quiz_bp = Blueprint("quiz", __name__)

QUIZ_BANK = {
    "Python": [
        {"id": 1, "q": "What is a Python decorator?", "options": ["A UI design pattern", "A function that modifies another function", "A type of loop", "A class method"], "answer": 1},
        {"id": 2, "q": "Which is used for list comprehension?", "options": ["[x for x in list]", "(x for x in list)", "{x for x in list}", "x => list"], "answer": 0},
        {"id": 3, "q": "What does `yield` do in Python?", "options": ["Returns a value and exits", "Creates a generator", "Raises an exception", "Imports a module"], "answer": 1},
        {"id": 4, "q": "What is GIL in Python?", "options": ["Global Interpreter Lock", "General Interface Library", "Global Index List", "None of the above"], "answer": 0},
    ],
    "JavaScript": [
        {"id": 1, "q": "What is closure in JavaScript?", "options": ["A method to close the browser", "A function accessing its outer scope", "A loop control statement", "An error type"], "answer": 1},
        {"id": 2, "q": "What does `async/await` handle?", "options": ["CSS animations", "Synchronous code only", "Asynchronous operations", "DOM manipulation"], "answer": 2},
        {"id": 3, "q": "What is event delegation?", "options": ["Assigning multiple events to one element", "Handling events on parent for children", "Removing event listeners", "Creating custom events"], "answer": 1},
        {"id": 4, "q": "What does `===` check?", "options": ["Value equality only", "Type equality only", "Value and type equality", "Reference equality"], "answer": 2},
    ],
    "React": [
        {"id": 1, "q": "What is a React Hook?", "options": ["An HTML attribute", "Function to use state in functional components", "A CSS property", "A component type"], "answer": 1},
        {"id": 2, "q": "What does useEffect do?", "options": ["Manages state", "Handles side effects in functional components", "Creates new components", "Styles components"], "answer": 1},
        {"id": 3, "q": "What is the Virtual DOM?", "options": ["Direct manipulation of HTML", "An in-memory representation of the real DOM", "A browser API", "A React database"], "answer": 1},
        {"id": 4, "q": "What does key prop do in lists?", "options": ["Styles list items", "Helps React identify changed elements", "Sorts the list", "Creates unique IDs"], "answer": 1},
    ],
    "Machine Learning": [
        {"id": 1, "q": "What is overfitting?", "options": ["Model too simple", "Model memorizes training data, fails on new data", "Model with no training", "A neural network type"], "answer": 1},
        {"id": 2, "q": "What is gradient descent?", "options": ["A tree algorithm", "Optimization to minimize loss function", "A preprocessing step", "A neural layer"], "answer": 1},
        {"id": 3, "q": "What does cross-validation do?", "options": ["Trains on all data", "Evaluates model on multiple data splits", "Cleans the dataset", "Normalizes features"], "answer": 1},
        {"id": 4, "q": "What is a confusion matrix?", "options": ["A data structure", "Table showing true vs predicted classifications", "A clustering method", "A loss function"], "answer": 1},
    ],
    "Docker": [
        {"id": 1, "q": "What is a Docker container?", "options": ["A virtual machine", "Lightweight standalone executable package", "A cloud service", "A network protocol"], "answer": 1},
        {"id": 2, "q": "What is a Dockerfile?", "options": ["Config file to build Docker images", "Container runtime", "Docker registry", "Docker network config"], "answer": 0},
        {"id": 3, "q": "What does `docker-compose` do?", "options": ["Builds single containers", "Defines and runs multi-container apps", "Pushes images to registry", "Creates Docker networks"], "answer": 1},
        {"id": 4, "q": "What is a Docker volume?", "options": ["Container memory", "Persistent data storage for containers", "Network bridge", "Docker image layer"], "answer": 1},
    ],
    "SQL": [
        {"id": 1, "q": "What does JOIN do in SQL?", "options": ["Deletes records", "Combines rows from two or more tables", "Creates a new table", "Filters records"], "answer": 1},
        {"id": 2, "q": "What is an INDEX in SQL?", "options": ["A table column", "Data structure to speed up queries", "A primary key constraint", "A foreign key"], "answer": 1},
        {"id": 3, "q": "Difference between WHERE and HAVING?", "options": ["No difference", "WHERE filters rows, HAVING filters groups", "HAVING filters rows, WHERE filters groups", "Both filter groups"], "answer": 1},
        {"id": 4, "q": "What is a transaction in SQL?", "options": ["A single query", "A unit of work that is atomic", "A stored procedure", "A view"], "answer": 1},
    ],
    "AWS": [
        {"id": 1, "q": "What is Amazon S3?", "options": ["A compute service", "Object storage service", "Database service", "CDN service"], "answer": 1},
        {"id": 2, "q": "What is an EC2 instance?", "options": ["Storage bucket", "Virtual server in the cloud", "DNS service", "Email service"], "answer": 1},
        {"id": 3, "q": "What does IAM stand for?", "options": ["Internet Access Management", "Identity and Access Management", "Internal Application Monitor", "Integrated API Manager"], "answer": 1},
        {"id": 4, "q": "What is AWS Lambda?", "options": ["A database", "Serverless compute service", "Container service", "Load balancer"], "answer": 1},
    ],
    "MongoDB": [
        {"id": 1, "q": "What type of database is MongoDB?", "options": ["Relational", "Document-based NoSQL", "Graph database", "Key-value store"], "answer": 1},
        {"id": 2, "q": "What is a MongoDB collection?", "options": ["A row in a table", "Equivalent to a table in relational DB", "A database backup", "A MongoDB query"], "answer": 1},
        {"id": 3, "q": "What does `$match` do in aggregation?", "options": ["Joins collections", "Filters documents", "Groups documents", "Sorts documents"], "answer": 1},
        {"id": 4, "q": "What is an ObjectId in MongoDB?", "options": ["A string field", "Default unique identifier for documents", "An index type", "A collection name"], "answer": 1},
    ]
}

DEFAULT_QUESTIONS = [
    {"id": 1, "q": "What is a REST API?", "options": ["A database type", "An architectural style for networked applications", "A programming language", "A frontend framework"], "answer": 1},
    {"id": 2, "q": "What does HTTP 404 mean?", "options": ["Server error", "Resource not found", "Unauthorized", "Success"], "answer": 1},
    {"id": 3, "q": "What is version control?", "options": ["Controlling app versions in production", "System to track changes in source code", "A deployment strategy", "A testing method"], "answer": 1},
    {"id": 4, "q": "What is the purpose of unit testing?", "options": ["Test entire application", "Test individual components in isolation", "Test user interface", "Load test the server"], "answer": 1},
]


@quiz_bp.route("/questions/<skill>", methods=["GET"])
@jwt_required()
def get_questions(skill):
    questions = QUIZ_BANK.get(skill, DEFAULT_QUESTIONS)
    # Return questions without answers
    safe_questions = [{"id": q["id"], "q": q["q"], "options": q["options"]} for q in questions]
    return jsonify({"skill": skill, "questions": safe_questions, "total": len(safe_questions)}), 200


@quiz_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_quiz():
    user_id = get_jwt_identity()
    data = request.get_json()
    skill = data.get("skill", "")
    answers = data.get("answers", {})  # {question_id: answer_index}

    if not skill:
        return jsonify({"error": "Skill is required"}), 400

    questions = QUIZ_BANK.get(skill, DEFAULT_QUESTIONS)
    score = 0
    results = []

    for q in questions:
        q_id = str(q["id"])
        user_answer = answers.get(q_id)
        correct = q["answer"]
        is_correct = user_answer == correct
        if is_correct:
            score += 1
        results.append({
            "question_id": q["id"],
            "question": q["q"],
            "your_answer": user_answer,
            "correct_answer": correct,
            "correct_option": q["options"][correct],
            "is_correct": is_correct
        })

    total = len(questions)
    passed = score >= round(total * 0.6)
    percentage = round((score / total) * 100, 1)

    # Save attempt to DB
    SkillVerificationModel.save_attempt(user_id, skill, score, total, passed)

    # If passed, add to user's verified skills
    if passed:
        UserModel.add_verified_skill(user_id, skill)

    return jsonify({
        "skill": skill,
        "score": score,
        "total": total,
        "percentage": percentage,
        "passed": passed,
        "results": results,
        "message": f"{'✓ Skill Verified!' if passed else 'Not verified. Try again!'}"
    }), 200


@quiz_bp.route("/verified", methods=["GET"])
@jwt_required()
def get_verified_skills():
    user_id = get_jwt_identity()
    verifications = SkillVerificationModel.get_user_verifications(user_id)
    verified_skills = list({v["skill"] for v in verifications})
    return jsonify({"verified_skills": verified_skills}), 200


@quiz_bp.route("/attempts/<skill>", methods=["GET"])
@jwt_required()
def get_attempts(skill):
    user_id = get_jwt_identity()
    attempts = SkillVerificationModel.get_attempts(user_id, skill)
    return jsonify({"skill": skill, "attempts": attempts}), 200


@quiz_bp.route("/available-skills", methods=["GET"])
def available_skills():
    return jsonify({"skills": list(QUIZ_BANK.keys())}), 200
