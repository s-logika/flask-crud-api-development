from flask import Blueprint, request, jsonify
from app.controllers.student_controller import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
)

student_bp = Blueprint("students", __name__)


@student_bp.route("/api/students", methods=["POST"])
def create_student_route():
    student, error = create_student(request.get_json())
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": "Student created.", "student": student.to_dict()}), 201


@student_bp.route("/api/students", methods=["GET"])
def get_students_route():
    students = get_all_students()
    if not students:
        return jsonify({"message": "No students found.", "students": []}), 200
    return jsonify({"students": [s.to_dict() for s in students]}), 200


@student_bp.route("/api/students/<int:id>", methods=["GET"])
def get_student_route(id):
    student = get_student_by_id(id)
    if not student:
        return jsonify({"error": f"Student with id {id} not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


@student_bp.route("/api/students/<int:id>", methods=["PUT"])
def update_student_route(id):
    student, error = update_student(id, request.get_json())
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": "Student updated.", "student": student.to_dict()}), 200


@student_bp.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student_route(id):
    student, error = delete_student(id)
    if error:
        return jsonify({"error": error[0]}), error[1]
    return jsonify({"message": f"Student '{student.full_name}' deleted successfully."}), 200
