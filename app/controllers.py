from flask import request, jsonify
from datetime import datetime
from models import db, Student, Course


# ─────────────────────────────────────────
# Student Controllers
# ─────────────────────────────────────────

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

    existing = Student.query.filter_by(email=data["email"]).first()

    if existing:
        return jsonify({"error": "Email already exists."}), 409

    try:
        joined = datetime.strptime(
            data["joined_date"],
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return jsonify({
            "error": "joined_date must be YYYY-MM-DD format."
        }), 400

    student = Student(
        full_name=data["full_name"],
        email=data["email"],
        age=data["age"],
        cgpa=data.get("cgpa", 0.0),
        is_active=data.get("is_active", True),
        joined_date=joined
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created.",
        "student": student.to_dict()
    }), 201


def get_students():

    students = Student.query.all()

    return jsonify({
        "students": [s.to_dict() for s in students]
    }), 200


def get_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "error": f"Student with id {id} not found."
        }), 404

    return jsonify({
        "student": student.to_dict()
    }), 200


def update_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "error": f"Student with id {id} not found."
        }), 404

    data = request.get_json()

    if "full_name" in data:
        student.full_name = data["full_name"]

    if "email" in data:
        student.email = data["email"]

    if "age" in data:
        student.age = data["age"]

    if "cgpa" in data:
        student.cgpa = data["cgpa"]

    db.session.commit()

    return jsonify({
        "message": "Student updated.",
        "student": student.to_dict()
    }), 200


def delete_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "error": f"Student with id {id} not found."
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully."
    }), 200


# ─────────────────────────────────────────
# Course Controllers
# ─────────────────────────────────────────

def create_course():

    data = request.get_json()

    course = Course(
        course_title=data["course_title"],
        course_fee=data["course_fee"],
        duration_months=data["duration_months"],
        description=data.get("description"),
        is_available=data.get("is_available", True)
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created.",
        "course": course.to_dict()
    }), 201


def get_courses():

    courses = Course.query.all()

    return jsonify({
        "courses": [c.to_dict() for c in courses]
    }), 200


def get_course(id):

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "error": f"Course with id {id} not found."
        }), 404

    return jsonify({
        "course": course.to_dict()
    }), 200


def update_course(id):

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "error": f"Course with id {id} not found."
        }), 404

    data = request.get_json()

    if "course_title" in data:
        course.course_title = data["course_title"]

    if "course_fee" in data:
        course.course_fee = data["course_fee"]

    if "duration_months" in data:
        course.duration_months = data["duration_months"]

    if "description" in data:
        course.description = data["description"]

    db.session.commit()

    return jsonify({
        "message": "Course updated.",
        "course": course.to_dict()
    }), 200


def delete_course(id):

    course = Course.query.get(id)

    if not course:
        return jsonify({
            "error": f"Course with id {id} not found."
        }), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully."
    }), 200