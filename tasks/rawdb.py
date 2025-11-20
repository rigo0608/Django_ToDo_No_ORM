import sqlite3
from pathlib import Path

# Path to the SQLite database file
DB_PATH = Path(__file__).resolve().parent.parent / "db.sqlite3"

# ----------------------
# Get database connection
# ----------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So we can access columns by name
    return conn

# ----------------------
# Convert a DB row to a Python dictionary
# ----------------------
def row_to_dict(row):
    return {k: row[k] for k in row.keys()}

# ----------------------
# Initialize the database and create tables
# ----------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Create tasks table if it doesn't exist
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

# ----------------------
# Run this file directly to initialize DB
# ----------------------
if __name__ == '__main__':
    init_db()
