from controllers import (
    create_student,
    get_students,
    get_student,
    update_student,
    delete_student,
    create_course,
    get_courses,
    get_course,
    update_course,
    delete_course
)


def register_routes(app):

    # Student Routes
    app.add_url_rule(
        "/api/students",
        view_func=create_student,
        methods=["POST"]
    )

    app.add_url_rule(
        "/api/students",
        view_func=get_students,
        methods=["GET"]
    )

    app.add_url_rule(
        "/api/students/<int:id>",
        view_func=get_student,
        methods=["GET"]
    )

    app.add_url_rule(
        "/api/students/<int:id>",
        view_func=update_student,
        methods=["PUT"]
    )

    app.add_url_rule(
        "/api/students/<int:id>",
        view_func=delete_student,
        methods=["DELETE"]
    )

    # Course Routes
    app.add_url_rule(
        "/api/courses",
        view_func=create_course,
        methods=["POST"]
    )

    app.add_url_rule(
        "/api/courses",
        view_func=get_courses,
        methods=["GET"]
    )

    app.add_url_rule(
        "/api/courses/<int:id>",
        view_func=get_course,
        methods=["GET"]
    )

    app.add_url_rule(
        "/api/courses/<int:id>",
        view_func=update_course,
        methods=["PUT"]
    )

    app.add_url_rule(
        "/api/courses/<int:id>",
        view_func=delete_course,
        methods=["DELETE"]
    )