# Django To-Do App (No ORM)

This project implements a To-Do list web application using Django but **without Django ORM**.
All database access is done with raw SQLite queries.

## Features
- CRUD APIs returning JSON
- HTML templates that use the APIs via fetch()
- SQLite DB (`db.sqlite3`) with `tasks` table
- Tests implemented using pytest + pytest-django

## Setup
1. Create virtualenv and install:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Initialize DB:
   ```
   python manage.py shell -c "from tasks.rawdb import init_db; init_db()"
   ```

3. Run server:
   ```
   python manage.py runserver
   ```

4. Run tests:
   ```
   pytest -q
   ```

## API Endpoints
- GET /api/tasks/        - list tasks
- GET /api/tasks/<id>/   - get one task
- POST /api/tasks/create/- create task (JSON)
- PUT /api/tasks/update/<id>/- update (JSON)
- DELETE /api/tasks/delete/<id>/- delete

Request/response examples are in API_DOC.md

