import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Use Railway PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")  # Fix for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Model
class CareerHelp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    linkedin_id = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=False)
    how_do_you_know_me = db.Column(db.String(255), nullable=False)
    referrer_name = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(255), nullable=True)
    current_status = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create tables
with app.app_context():
    db.create_all()

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        new_entry = CareerHelp(
            name=data["name"],
            linkedin_id=data["linkedinID"],
            university=data["university"],
            how_do_you_know_me=data["connectionType"],
            referrer_name=data.get("referral_name"),
            experience=data["growthStory"],
            company=data.get("companyName"),
            role=data.get("role"),
            current_status=data["currentStatus"]
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data saved successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/entries", methods=["GET"])
def get_entries():
    entries = CareerHelp.query.all()
    return jsonify([
        {
            "name": entry.name,
            "linkedin_id": entry.linkedin_id,
            "university": entry.university,
            "how_do_you_know_me": entry.how_do_you_know_me,
            "referrer_name": entry.referrer_name,
            "experience": entry.experience,
            "company": entry.company,
            "role": entry.role,
            "current_status": entry.current_status,
            "created_at": entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for entry in entries
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
