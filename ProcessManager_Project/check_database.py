import sqlite3
from database import DATABASE_NAME

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

cursor.execute("""
    SELECT timestamp, pid, process_name, process_type,
           cpu_percent, memory_mb, io_rate, classification
    FROM process_history
    ORDER BY timestamp DESC
    LIMIT 10
""")

rows = cursor.fetchall()

print("\nLatest saved process records:")
for row in rows:
    print(row)

print("\nTotal records:", end=" ")
cursor.execute("SELECT COUNT(*) FROM process_history")
print(cursor.fetchone()[0])

connection.close()
