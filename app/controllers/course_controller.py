from app import db
from app.models.course_model import Course


def create_course(data):
    if not data:
        return None, ("No data provided.", 400)
    if not data.get("course_title"):
        return None, ("course_title is required.", 400)
    if data.get("course_fee") is None:
        return None, ("course_fee is required.", 400)
    if data.get("duration_months") is None:
        return None, ("duration_months is required.", 400)
    if not isinstance(data["course_fee"], (int, float)) or data["course_fee"] <= 0:
        return None, ("course_fee must be a positive number.", 400)
    if not isinstance(data["duration_months"], int) or data["duration_months"] <= 0:
        return None, ("duration_months must be a positive integer.", 400)
    if Course.query.filter_by(course_title=data["course_title"]).first():
        return None, ("Course title already exists.", 409)

    course = Course(
        course_title=data["course_title"],
        course_fee=data["course_fee"],
        duration_months=data["duration_months"],
        description=data.get("description"),
        is_available=data.get("is_available", True),
    )
    db.session.add(course)
    db.session.commit()
    return course, None


def get_all_courses():
    return Course.query.all()


def get_course_by_id(course_id):
    return Course.query.get(course_id)


def update_course(course_id, data):
    course = Course.query.get(course_id)
    if not course:
        return None, (f"Course with id {course_id} not found.", 404)
    if not data:
        return None, ("No data provided.", 400)

    if "course_title" in data:
        existing = Course.query.filter_by(course_title=data["course_title"]).first()
        if existing and existing.id != course_id:
            return None, ("Course title already exists.", 409)
        course.course_title = data["course_title"]

    if "course_fee" in data:
        if not isinstance(data["course_fee"], (int, float)) or data["course_fee"] <= 0:
            return None, ("course_fee must be a positive number.", 400)
        course.course_fee = data["course_fee"]

    if "duration_months" in data:
        if not isinstance(data["duration_months"], int) or data["duration_months"] <= 0:
            return None, ("duration_months must be a positive integer.", 400)
        course.duration_months = data["duration_months"]

    if "description" in data:
        course.description = data["description"]

    if "is_available" in data:
        course.is_available = data["is_available"]

    db.session.commit()
    return course, None


def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return None, (f"Course with id {course_id} not found.", 404)
    db.session.delete(course)
    db.session.commit()
    return course, None
