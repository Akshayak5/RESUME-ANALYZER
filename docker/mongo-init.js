db = db.getSiblingDB("resumeiq");

// Create collections
db.createCollection("users");
db.createCollection("resumes");
db.createCollection("test_results");

// User indexes
db.users.createIndex({ email: 1 }, { unique: true });

// Resume indexes
db.resumes.createIndex({ user_id: 1 });
db.resumes.createIndex({ "analysis.skills": 1 });
db.resumes.createIndex({ "analysis.score.total": -1 });
db.resumes.createIndex({ uploaded_at: -1 });

// Skill test indexes
db.test_results.createIndex({ user_id: 1, skill: 1 });

print("✅ ResumeIQ DB ready!");