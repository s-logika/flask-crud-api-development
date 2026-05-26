# Flask + MySQL CRUD API

A REST API built with **Flask**, **MySQL**, and **SQLAlchemy ORM** that manages Students and Courses.

---

## Project Structure

```
crud-api-dev/
├── .env               ← you create this (not on GitHub)
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── app/
    ├── __init__.py
    ├── config.py
    ├── models/
    │   ├── __init__.py
    │   ├── student_model.py
    │   └── course_model.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── student_controller.py
    │   └── course_controller.py
    └── routes/
        ├── __init__.py
        ├── student_routes.py
        └── course_routes.py
```

| File / Folder | Purpose |
| --- | --- |
| `run.py` | Entry point — starts the Flask app |
| `app/__init__.py` | App factory, initializes DB, registers blueprints |
| `app/config.py` | Database config loaded from `.env` |
| `app/models/` | SQLAlchemy model definitions |
| `app/controllers/` | Business logic and DB operations |
| `app/routes/` | Flask Blueprints — URL routing |

---

## Requirements

- Python 3.8+
- MySQL Server
- pip

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/s-logika/flask-crud-api-development.git
cd flask-crud-api-development
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database in MySQL

```sql
CREATE DATABASE flask_crud_db;
```

### 5. Create your `.env` file

Create a file named `.env` in the project root and add your MySQL credentials:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=flask_crud_db
```

> **Note:** Never share your `.env` file. It is listed in `.gitignore` and will not be pushed to GitHub.

### 6. Run the application

```bash
python run.py
```

You should see:

```
Tables ready.
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Tables are created automatically on startup.

---

## API Testing

Use **Thunder Client** (VS Code extension) or **Postman** to test the endpoints.

**Base URL:** `http://127.0.0.1:5000`

---

## Student Endpoints

### POST `/api/students` — Create a student

**Request body:**

```json
{
    "full_name": "Ali Hassan",
    "email": "ali@test.com",
    "age": 22,
    "cgpa": 3.5,
    "joined_date": "2024-01-15"
}
```

**Success response — 201:**

```json
{
    "message": "Student created.",
    "student": {
        "id": 1,
        "full_name": "Ali Hassan",
        "email": "ali@test.com",
        "age": 22,
        "cgpa": 3.5,
        "is_active": true,
        "joined_date": "2024-01-15",
        "created_at": "2024-01-15 10:30:00"
    }
}
```

**Validation errors:**

| Scenario | Status | Response |
| --- | --- | --- |
| Missing `full_name` | 400 | `{"error": "full_name is required."}` |
| Missing `email` | 400 | `{"error": "email is required."}` |
| Missing `age` | 400 | `{"error": "age is required."}` |
| Missing `joined_date` | 400 | `{"error": "joined_date is required."}` |
| Negative age | 400 | `{"error": "age must be a positive integer."}` |
| Duplicate email | 409 | `{"error": "Email already exists."}` |
| Wrong date format | 400 | `{"error": "joined_date must be YYYY-MM-DD format."}` |

---

### GET `/api/students` — Get all students

**Success response — 200:**

```json
{
  "students": [
    { "id": 1, "full_name": "Ali Hassan", "email": "ali@test.com", ... },
    { "id": 2, "full_name": "Sara Ahmed", "email": "sara@test.com", ... }
  ]
}
```

---

### GET `/api/students/<id>` — Get one student

Example: `GET /api/students/1`

**Success response — 200:**

```json
{
  "student": {
    "id": 1,
    "full_name": "Ali Hassan",
    ...
  }
}
```

**Not found — 404:**

```json
{ "error": "Student with id 1 not found." }
```

---

### PUT `/api/students/<id>` — Update a student

Example: `PUT /api/students/1`

Only send the fields you want to update:

```json
{
    "full_name": "Ali Hassan Updated",
    "cgpa": 3.8
}
```

**Success response — 200:**

```json
{
  "message": "Student updated.",
  "student": { ... }
}
```

**Validation errors:**

| Scenario | Status | Response |
| --- | --- | --- |
| ID not found | 404 | `{"error": "Student with id 1 not found."}` |
| Empty request body | 400 | `{"error": "No data provided."}` |
| Duplicate email | 409 | `{"error": "Email already exists."}` |

---

### DELETE `/api/students/<id>` — Delete a student

Example: `DELETE /api/students/1`

**Success response — 200:**

```json
{ "message": "Student 'Ali Hassan' deleted successfully." }
```

**Not found — 404:**

```json
{ "error": "Student with id 1 not found." }
```

---

## Course Endpoints

### POST `/api/courses` — Create a course

**Request body:**

```json
{
    "course_title": "Python Basics",
    "course_fee": 500.0,
    "duration_months": 3,
    "description": "Introduction to Python programming."
}
```

**Success response — 201:**

```json
{
    "message": "Course created.",
    "course": {
        "id": 1,
        "course_title": "Python Basics",
        "course_fee": 500.0,
        "duration_months": 3,
        "description": "Introduction to Python programming.",
        "is_available": true,
        "created_at": "2024-01-15 10:30:00"
    }
}
```

**Validation errors:**

| Scenario | Status | Response |
| --- | --- | --- |
| Missing `course_title` | 400 | `{"error": "course_title is required."}` |
| Missing `course_fee` | 400 | `{"error": "course_fee is required."}` |
| Missing `duration_months` | 400 | `{"error": "duration_months is required."}` |
| Negative fee | 400 | `{"error": "course_fee must be a positive number."}` |
| Zero or negative duration | 400 | `{"error": "duration_months must be a positive integer."}` |
| Duplicate title | 409 | `{"error": "Course title already exists."}` |

---

### GET `/api/courses` — Get all courses

**Success response — 200:**

```json
{
  "courses": [
    { "id": 1, "course_title": "Python Basics", ... },
    { "id": 2, "course_title": "Flask Web Dev", ... }
  ]
}
```

---

### GET `/api/courses/<id>` — Get one course

Example: `GET /api/courses/1`

**Success response — 200:**

```json
{
  "course": {
    "id": 1,
    "course_title": "Python Basics",
    ...
  }
}
```

**Not found — 404:**

```json
{ "error": "Course with id 1 not found." }
```

---

### PUT `/api/courses/<id>` — Update a course

Example: `PUT /api/courses/1`

Only send the fields you want to update:

```json
{
    "course_fee": 600.0,
    "is_available": false
}
```

**Success response — 200:**

```json
{
  "message": "Course updated.",
  "course": { ... }
}
```

**Validation errors:**

| Scenario | Status | Response |
| --- | --- | --- |
| ID not found | 404 | `{"error": "Course with id 1 not found."}` |
| Empty request body | 400 | `{"error": "No data provided."}` |
| Duplicate title | 409 | `{"error": "Course title already exists."}` |

---

### DELETE `/api/courses/<id>` — Delete a course

Example: `DELETE /api/courses/1`

**Success response — 200:**

```json
{ "message": "Course 'Python Basics' deleted successfully." }
```

**Not found — 404:**

```json
{ "error": "Course with id 1 not found." }
```

---

## All Endpoints Summary

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/students` | Create a student |
| GET | `/api/students` | Get all students |
| GET | `/api/students/<id>` | Get one student |
| PUT | `/api/students/<id>` | Update a student |
| DELETE | `/api/students/<id>` | Delete a student |
| POST | `/api/courses` | Create a course |
| GET | `/api/courses` | Get all courses |
| GET | `/api/courses/<id>` | Get one course |
| PUT | `/api/courses/<id>` | Update a course |
| DELETE | `/api/courses/<id>` | Delete a course |

---

## Tech Stack

- **Python** — programming language
- **Flask** — web framework
- **MySQL** — database
- **SQLAlchemy** — ORM (Object Relational Mapper)
- **PyMySQL** — MySQL connector for Python
- **python-dotenv** — loads `.env` variables
