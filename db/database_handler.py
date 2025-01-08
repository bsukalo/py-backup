import sqlite3

DB_FILE = "backup_metadata.db"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY,
    file_path TEXT,
    file_hash TEXT UNIQUE,
    backup_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
)

connection.commit()


def insert_backup_metadata(file_path, file_hash):
    cursor.execute(
        "INSERT INTO backups (file_path, file_hash) VALUES (?, ?)",
        (file_path, file_hash),
    )
    connection.commit()


def check_duplicate(file_hash):
    cursor.execute("SELECT * FROM backups WHERE file_hash = ?", (file_hash,))
    return cursor.fetchone() is not None


def get_all_backups():
    cursor.execute("SELECT file_path, file_hash, backup_time FROM backups")
    backups = cursor.fetchall()

    # returns data as list of directories
    return [
        {
            "file_path": row[0],
            "file_hash": row[1],
            "backup_time": row[2],
        }
        for row in backups
    ]
