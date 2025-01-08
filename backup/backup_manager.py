import shutil
import os
import hashlib
from db.database_handler import insert_backup_metadata

BACKUP_DIR = "backups/"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)


def create_backup(file_path):
    file_hash = compute_file_hash(file_path)
    dest_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))

    if not is_duplicate(file_hash):
        shutil.copy(file_path, dest_path)
        insert_backup_metadata(file_path, file_hash)
        print(f"Backup completed for {file_path}")
    else:
        print(f"Duplicate file detected: {file_path}, skipping backup.")


def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def is_duplicate(file_hash):
    from db.database_handler import check_duplicate

    return check_duplicate(file_hash)


# file recovery function
def recover_file(backup):
    backup_dir = "backups/"
    original_path = backup["file_path"]
    backup_path = os.path.join(backup_dir, os.path.basename(original_path))

    if not os.path.exists(backup_path):
        print(f"Backup file not found: {backup_path}")
        return

    target_dir = os.path.dirname(original_path)
    if not os.path.exists(target_dir):
        print(f"Original directory not found: {target_dir}")
        print("Creating the directory...")
        os.makedirs(target_dir)

    shutil.copy(backup_path, original_path)
    print(f"Recovered file to: {original_path}")
