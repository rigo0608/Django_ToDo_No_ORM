# Django To-Do App (No ORM)

## Overview

This is a simple **To-Do application** built with **Django 4.2** without using the Django ORM.
All database operations are done using **raw SQL** via SQLite.
The application provides both **web pages** and **RESTful APIs** for task management.

**Features:**

* Create, read, update, and delete tasks
* Web pages for adding and editing tasks
* REST APIs for full CRUD functionality
* Input validation for `title` and `due_date`
* Status normalization (`pending` or `completed`)
* Simple and lightweight (no ORM overhead)

---

## Setup

1. **Clone the repository**

```
git clone <your-repo-url>
cd django_todo_no_orm
```

2. **Create a virtual environment**

```
python -m venv venv
```

3. **Activate virtual environment**

* Windows:

```
venv\Scripts\activate
```

* Linux/macOS:

```
source venv/bin/activate
```

4. **Install dependencies**

```
pip install -r requirements.txt
```

5. **Apply database setup**

```
python manage.py migrate
```

> Note: Tables are created manually in `rawdb.py` or via initial SQL scripts.

6. **Run the server**

```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the app.

---

## APIs

**Base URL:** `http://127.0.0.1:8000/`

### 1. List Tasks

* **Endpoint:** `GET /api/tasks/`
* **Response:** `200 OK`

```
[
  { "id":1, "title":"Task 1", "description":"", "due_date":null, "status":"pending" },
  ...
]
```

### 2. Get Task by ID

* **Endpoint:** `GET /api/tasks/<id>/`
* **Response:** `200 OK` or `404 Not Found`

### 3. Create Task

* **Endpoint:** `POST /api/tasks/create/`
* **Content-Type:** `application/json`
* **Body:**

```
{
  "title": "Buy milk",
  "description": "2 liters",
  "due_date": "2025-11-25",
  "status": "pending"
}
```

* **Response:** `201 Created` with created task object

### 4. Update Task

* **Endpoint:** `PUT /api/tasks/update/<id>/`
* **Content-Type:** `application/json`
* **Body:** Any combination of `title`, `description`, `due_date`, `status`
* **Response:** `200 OK` or `404 Not Found`

### 5. Delete Task

* **Endpoint:** `DELETE /api/tasks/delete/<id>/`
* **Response:** `200 OK` or `404 Not Found`

**Notes:**

* No authentication implemented
* Uses raw SQL with prepared statements to prevent SQL injection

---

## Testing

1. **Run unit tests**

```
pytest tasks/tests/test_tasks.py -v
```

2. **Expected results**

* All 13 test cases should pass
* Includes tests for valid CRUD operations and error cases:

  * Missing title
  * Invalid due date
  * Updating non-existent task
  * Updating nothing

---

## Deployment Notes

* Can be deployed on any server supporting Python 3.12+ and Django 4.2
* Ensure SQLite database file is present or created
* No additional configuration required for default setup
* For production, configure `ALLOWED_HOSTS` in `settings.py` and use `gunicorn`/`nginx`

---

## Additional Notes

* This project demonstrates **Django without ORM**, using **raw SQL**
* Useful for learning:

  * Direct database operations
  * RESTful API design
  * Input validation and error handling

