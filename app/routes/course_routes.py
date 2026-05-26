from flask import Blueprint, request, jsonify
from app.controllers.course_controller import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course,
)

course_bp = Blueprint("courses", __name__)


@course_bp.route("/api/courses", methods=["POST"])
def create_course_route():
    course, error = create_course(request.get_json())
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": "Course created.", "course": course.to_dict()}), 201


@course_bp.route("/api/courses", methods=["GET"])
def get_courses_route():
    courses = get_all_courses()
    if not courses:
        return jsonify({"message": "No courses found.", "courses": []}), 200
    return jsonify({"courses": [c.to_dict() for c in courses]}), 200


@course_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_course_route(id):
    course = get_course_by_id(id)
    if not course:
        return jsonify({"error": f"Course with id {id} not found."}), 404
    return jsonify({"course": course.to_dict()}), 200


@course_bp.route("/api/courses/<int:id>", methods=["PUT"])
def update_course_route(id):
    course, error = update_course(id, request.get_json())
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": "Course updated.", "course": course.to_dict()}), 200


@course_bp.route("/api/courses/<int:id>", methods=["DELETE"])
def delete_course_route(id):
    course, error = delete_course(id)
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": f"Course '{course.course_title}' deleted successfully."}), 200
