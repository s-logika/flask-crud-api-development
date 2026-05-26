from datetime import datetime
from app import db
from app.models.student_model import Student


def create_student(data):
    if not data:
        return None, ("No data provided.", 400)
    if not data.get("full_name"):
        return None, ("full_name is required.", 400)
    if not data.get("email"):
        return None, ("email is required.", 400)
    if data.get("age") is None:
        return None, ("age is required.", 400)
    if not data.get("joined_date"):
        return None, ("joined_date is required.", 400)
    if not isinstance(data["age"], int) or data["age"] <= 0:
        return None, ("age must be a positive integer.", 400)
    if Student.query.filter_by(email=data["email"]).first():
        return None, ("Email already exists.", 409)
    try:
        joined = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
    except ValueError:
        return None, ("joined_date must be YYYY-MM-DD format.", 400)

    student = Student(
        full_name=data["full_name"],
        email=data["email"],
        age=data["age"],
        cgpa=data.get("cgpa", 0.0),
        is_active=data.get("is_active", True),
        joined_date=joined,
    )
    db.session.add(student)
    db.session.commit()
    return student, None


def get_all_students():
    return Student.query.all()


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def update_student(student_id, data):
    student = Student.query.get(student_id)
    if not student:
        return None, (f"Student with id {student_id} not found.", 404)
    if not data:
        return None, ("No data provided.", 400)

    if "full_name" in data:
        if not data["full_name"]:
            return None, ("full_name cannot be empty.", 400)
        student.full_name = data["full_name"]

    if "email" in data:
        existing = Student.query.filter_by(email=data["email"]).first()
        if existing and existing.id != student_id:
            return None, ("Email already exists.", 409)
        student.email = data["email"]

    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] <= 0:
            return None, ("age must be a positive integer.", 400)
        student.age = data["age"]

    if "cgpa" in data:
        student.cgpa = data["cgpa"]

    if "is_active" in data:
        student.is_active = data["is_active"]

    if "joined_date" in data:
        try:
            student.joined_date = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
        except ValueError:
            return None, ("joined_date must be YYYY-MM-DD format.", 400)

    db.session.commit()
    return student, None


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return None, (f"Student with id {student_id} not found.", 404)
    db.session.delete(student)
    db.session.commit()
    return student, None
