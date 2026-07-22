import sqlite3
import os
import sys

# Try to find the db.sqlite3 file
db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print("Database not found!")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.execute("SELECT id, document_type, original_filename FROM services_document ORDER BY id DESC LIMIT 10")
    for row in cursor.fetchall():
        print(row)
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    conn.close()
