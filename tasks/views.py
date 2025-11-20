import logging, json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .rawdb import get_conn, row_to_dict

logger = logging.getLogger(__name__)

# --------------------
#   HEALTH CHECK
# --------------------
def health(request):
    # Simple API to check if server is running
    return JsonResponse({'status': 'ok'})


# --------------------
#   PAGES
# --------------------
def index(request):
    # Home page showing all tasks
    return render(request, 'index.html')


def add_page(request):
    # Page to add a new task
    return render(request, 'form.html', {'task_id': None})


def edit_page(request, task_id):
    # Page to edit an existing task
    return render(request, 'form.html', {'task_id': task_id})


# --------------------
#   API: GET ALL TASKS
# --------------------
def api_get_tasks(request):
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks ORDER BY id ASC")
        rows = cur.fetchall()

        tasks = []
        display_id = 1
        for r in rows:
            t = row_to_dict(r)
            # Normalize status
            t["status"] = (t.get("status") or "pending").lower()
            if t["status"] not in ["pending", "completed"]:
                t["status"] = "pending"
            # Assign display ID
            t["display_id"] = display_id
            display_id += 1
            tasks.append(t)

        return JsonResponse(tasks, safe=False, status=200)

    except Exception:
        logger.exception("Failed to list tasks")
        return JsonResponse({'error': 'internal'}, status=500)

    finally:
        if conn:
            conn.close()


# --------------------
#   API: GET ONE TASK
# --------------------
def api_get_task(request, task_id):
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        r = cur.fetchone()

        if not r:
            # Task not found
            return JsonResponse({'error': 'not found'}, status=404)

        t = row_to_dict(r)
        t["status"] = (t.get("status") or "pending").lower()
        if t["status"] not in ["pending", "completed"]:
            t["status"] = "pending"

        return JsonResponse(t, status=200)

    except Exception:
        logger.exception("Failed to get task")
        return JsonResponse({'error': 'internal'}, status=500)

    finally:
        if conn:
            conn.close()


# --------------------
#   API: CREATE TASK
# --------------------
@csrf_exempt
def api_create_task(request):
    if request.method != 'POST':
        # Only POST allowed
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'bad json'}, status=400)

    # Validate title
    title = payload.get('title')
    if not title:
        return JsonResponse({'error': 'title required'}, status=400)

    # Validate due_date
    due = payload.get('due_date')
    if due:
        try:
            datetime.fromisoformat(due)
        except ValueError:
            return JsonResponse({'error': 'invalid due_date'}, status=400)

    # Normalize status
    status = (payload.get('status') or 'pending').lower()
    if status not in ['pending', 'completed']:
        status = 'pending'

    description = payload.get('description') or ""

    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks(title, description, due_date, status) VALUES (?, ?, ?, ?)",
            (title, description, due, status)
        )
        conn.commit()
        new_id = cur.lastrowid
        # Fetch the created task
        cur.execute("SELECT * FROM tasks WHERE id=?", (new_id,))
        row = cur.fetchone()
        if not row:
            return JsonResponse({'error': 'internal'}, status=500)
        t = row_to_dict(row)
        t['status'] = status
        return JsonResponse(t, status=201)
    except Exception:
        logger.exception("Failed to create task")
        return JsonResponse({'error': 'internal'}, status=500)
    finally:
        if conn:
            conn.close()


# --------------------
#   API: UPDATE TASK
# --------------------
@csrf_exempt
def api_update_task(request, task_id):
    if request.method != 'PUT':
        # Only PUT allowed
        return JsonResponse({'error': 'PUT required'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'bad json'}, status=400)

    allowed = ['title', 'description', 'due_date', 'status']
    fields = []
    vals = []

    for key in allowed:
        if key in payload:
            val = payload[key]
            if key == 'due_date' and val:
                try:
                    datetime.fromisoformat(val)
                except ValueError:
                    return JsonResponse({'error': 'invalid due_date'}, status=400)
            if key == 'status':
                val = (val or 'pending').lower()
                if val not in ['pending', 'completed']:
                    val = 'pending'
            fields.append(f"{key}=?")
            vals.append(val)

    if not fields:
        # Nothing to update
        return JsonResponse({'error': 'nothing to update'}, status=400)

    vals.append(task_id)
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id=?"
        cur.execute(sql, tuple(vals))
        conn.commit()
        if cur.rowcount == 0:
            return JsonResponse({'error': 'not found'}, status=404)
        # Return updated task
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = cur.fetchone()
        if not row:
            return JsonResponse({'error': 'internal'}, status=500)
        t = row_to_dict(row)
        t['status'] = (t.get('status') or 'pending').lower()
        if t['status'] not in ['pending', 'completed']:
            t['status'] = 'pending'
        return JsonResponse(t, status=200)
    except Exception:
        logger.exception("Failed to update task")
        return JsonResponse({'error': 'internal'}, status=500)
    finally:
        if conn:
            conn.close()


# --------------------
#   API: DELETE TASK
# --------------------
@csrf_exempt
def api_delete_task(request, task_id):
    if request.method != 'DELETE':
        # Only DELETE allowed
        return JsonResponse({'error': 'DELETE required'}, status=405)

    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        if cur.rowcount == 0:
            return JsonResponse({'error': 'not found'}, status=404)
        return JsonResponse({'deleted': task_id}, status=200)
    except Exception:
        logger.exception("Failed to delete task")
        return JsonResponse({'error': 'internal'}, status=500)
    finally:
        if conn:
            conn.close()
