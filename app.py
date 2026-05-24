from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from datetime import datetime, date

class Student(db.Model):
    __tablename__ = "students"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name   = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), nullable=False, unique=True)
    age         = db.Column(db.Integer, nullable=False)
    cgpa        = db.Column(db.Float, default=0.0)
    is_active   = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "full_name":   self.full_name,
            "email":       self.email,
            "age":         self.age,
            "cgpa":        self.cgpa,
            "is_active":   self.is_active,
            "joined_date": str(self.joined_date),
            "created_at":  str(self.created_at),
        }

from flask import Flask, request, jsonify


# --- Student Routes ---
@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided."}), 400
    if not data.get("full_name"):
        return jsonify({"error": "full_name is required."}), 400
    if not data.get("email"):
        return jsonify({"error": "email is required."}), 400
    if data.get("age") is None:
        return jsonify({"error": "age is required."}), 400
    if not data.get("joined_date"):
        return jsonify({"error": "joined_date is required."}), 400

    if not isinstance(data["age"], int) or data["age"] <= 0:
        return jsonify({"error": "age must be a positive integer."}), 400

    existing = Student.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"error": "Email already exists."}), 409

    try:
        joined = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "joined_date must be YYYY-MM-DD format."}), 400

    student = Student(
        full_name   = data["full_name"],
        email       = data["email"],
        age         = data["age"],
        cgpa        = data.get("cgpa", 0.0),
        is_active   = data.get("is_active", True),
        joined_date = joined,
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student created.", "student": student.to_dict()}), 201

@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    if not students:
        return jsonify({"message": "No students found.", "students": []}), 200
    return jsonify({"students": [s.to_dict() for s in students]}), 200


@app.route("/api/students/", methods=["GET"])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": f"Student with id {id} not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


@app.route("/api/students/", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": f"Student with id {id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400

    if "full_name" in data:
        if not data["full_name"]:
            return jsonify({"error": "full_name cannot be empty."}), 400
        student.full_name = data["full_name"]

    if "email" in data:
        existing = Student.query.filter_by(email=data["email"]).first()
        if existing and existing.id != id:
            return jsonify({"error": "Email already exists."}), 409
        student.email = data["email"]

    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] <= 0:
            return jsonify({"error": "age must be a positive integer."}), 400
        student.age = data["age"]

    if "cgpa" in data:
        student.cgpa = data["cgpa"]

    if "is_active" in data:
        student.is_active = data["is_active"]

    if "joined_date" in data:
        try:
            student.joined_date = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "joined_date must be YYYY-MM-DD format."}), 400

    db.session.commit()
    return jsonify({"message": "Student updated.", "student": student.to_dict()}), 200



if __name__ == "__main__":
    app.run(debug=True)
    
    
# with app.app_context():
#     db.create_all()
#     print("Tables created!")