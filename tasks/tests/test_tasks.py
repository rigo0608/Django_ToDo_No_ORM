import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/tasks/"
CREATE_URL = "http://127.0.0.1:8000/api/tasks/create/"
UPDATE_URL = "http://127.0.0.1:8000/api/tasks/update/"
DELETE_URL = "http://127.0.0.1:8000/api/tasks/delete/"
HEALTH_URL = "http://127.0.0.1:8000/api/health/"

# ----------------------------
# Fixtures
# ----------------------------
@pytest.fixture(scope="module")
def task_data():
    return {
        "title": "No-ORM Pytest Task",
        "description": "Task created by pytest",
        "status": "pending",
        "due_date": "2025-12-31"
    }

@pytest.fixture(scope="module")
def created_task(task_data):
    # Create Task via API
    res = requests.post(CREATE_URL, json=task_data)
    assert res.status_code in (200, 201), f"Create failed: {res.status_code}, {res.text}"
    task = res.json()
    yield task
    # Cleanup: Delete Task if it still exists
    requests.delete(f"{DELETE_URL}{task['id']}/")

# ----------------------------
# Health Endpoint Test
# ----------------------------
def test_health():
    res = requests.get(HEALTH_URL)
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

# ----------------------------
# Create Task
# ----------------------------
def test_create_task(created_task, task_data):
    assert created_task["title"] == task_data["title"]
    assert created_task["status"] == task_data["status"]

def test_create_task_missing_title():
    res = requests.post(CREATE_URL, json={"description": "No title"})
    assert res.status_code == 400
    assert "title required" in res.text

def test_create_task_invalid_due_date(task_data):
    data = task_data.copy()
    data["due_date"] = "invalid-date"
    res = requests.post(CREATE_URL, json=data)
    assert res.status_code == 400
    assert "invalid due_date" in res.text

# ----------------------------
# Get Tasks
# ----------------------------
def test_get_tasks(created_task):
    res = requests.get(BASE_URL)
    assert res.status_code == 200
    tasks = res.json()
    assert any(t["id"] == created_task["id"] for t in tasks)

def test_get_task_by_id(created_task):
    res = requests.get(f"{BASE_URL}{created_task['id']}/")
    assert res.status_code == 200
    task = res.json()
    assert task["id"] == created_task["id"]
    assert task["title"] == created_task["title"]

def test_get_nonexistent_task():
    res = requests.get(f"{BASE_URL}999999/")
    assert res.status_code == 404
    assert "not found" in res.text

# ----------------------------
# Update Task
# ----------------------------
def test_update_task(created_task):
    update_payload = {
        "title": "Updated No-ORM Task",
        "description": "Updated description",
        "status": "completed"
    }
    res = requests.put(f"{UPDATE_URL}{created_task['id']}/", json=update_payload)
    assert res.status_code == 200
    updated_task = res.json()
    assert updated_task["title"] == update_payload["title"]
    assert updated_task["status"] == update_payload["status"]

def test_update_nonexistent_task():
    res = requests.put(f"{UPDATE_URL}999999/", json={"title": "test"})
    assert res.status_code == 404
    assert "not found" in res.text

def test_update_invalid_due_date(created_task):
    res = requests.put(f"{UPDATE_URL}{created_task['id']}/", json={"due_date": "abc"})
    assert res.status_code == 400
    assert "invalid due_date" in res.text

def test_update_nothing(created_task):
    res = requests.put(f"{UPDATE_URL}{created_task['id']}/", json={})
    assert res.status_code == 400
    assert "nothing to update" in res.text

# ----------------------------
# Delete Task
# ----------------------------
def test_delete_task(created_task):
    res = requests.delete(f"{DELETE_URL}{created_task['id']}/")
    assert res.status_code in (200, 204)
    # Verify deletion
    res = requests.get(BASE_URL)
    tasks = res.json()
    assert all(t["id"] != created_task["id"] for t in tasks)

def test_delete_nonexistent_task():
    res = requests.delete(f"{DELETE_URL}999999/")
    assert res.status_code == 404
    assert "not found" in res.text
