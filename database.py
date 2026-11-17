import sqlite3
import os
from datetime import datetime



DATABASE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "process_manager.db"
)


def initialize_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS process_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            pid INTEGER,
            process_name TEXT,
            process_type TEXT,
            cpu_percent REAL,
            memory_mb REAL,
            io_rate REAL,
            classification TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_processes(processes):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    records = []

    for process in processes:
        records.append((
            timestamp,
            process['pid'],
            process['name'],
            process['type'],
            process['cpu'],
            process['memory'],
            process['io_rate'],
            process['classification']
        ))

    cursor.executemany("""
        INSERT INTO process_history (
            timestamp, pid, process_name, process_type,
            cpu_percent, memory_mb, io_rate, classification
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    connection.commit()
    connection.close()
