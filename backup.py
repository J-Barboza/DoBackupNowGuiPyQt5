import os
import json
import datetime
import subprocess

SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"

def get_absolute_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def load_last_backup(last_backup_file):
    if os.path.exists(last_backup_file):
        with open(last_backup_file, 'r') as file:
            last_backup_info = json.load(file)
        return last_backup_info
    return {}

def save_last_backup(last_backup_file, backup_info):
    with open(last_backup_file, 'w') as file:
        json.dump(backup_info, file)

def get_modified_files(source_dirs, last_backup_time):
    modified_files = []
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            for foldername, subfolders, filenames in os.walk(source_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime > last_backup_time:
                        modified_files.append(file_path)
    return modified_files

def create_backup(source_dirs, backup_dest, incremental, last_backup_time, group_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    group_backup_dest = os.path.join(backup_dest, group_name)
    os.makedirs(group_backup_dest, exist_ok=True)
    backup_name = f"backup_{timestamp}.7z"
    backup_path = os.path.join(group_backup_dest, backup_name)
    
    if incremental:
        modified_files = get_modified_files(source_dirs, last_backup_time)
        if not modified_files:
            log_backup(f"No files modified since the last backup for group {group_name}.")
            return
        files_to_backup = modified_files
    else:
        files_to_backup = []
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                for foldername, subfolders, filenames in os.walk(source_dir):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        files_to_backup.append(file_path)

    files_to_backup_str = " ".join(f'"{file}"' for file in files_to_backup)
    command = f'"{SEVEN_ZIP_PATH}" a -spf "{backup_path}" {files_to_backup_str}'
    try:
        subprocess.run(command, check=True, shell=True)
        log_backup(f"Successfully backed up to {backup_path} for group {group_name}")
    except subprocess.CalledProcessError as e:
        log_backup(f"Error during backup for group {group_name}: {e}")

    return backup_path

def log_backup(message):
    with open("backup.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {message}\n")

def start_backup(source_dirs, backup_dest, incremental, group_name, backup_info):
    last_backup_time = backup_info.get(group_name, datetime.datetime.min)
    if isinstance(last_backup_time, str):
        last_backup_time = datetime.datetime.fromisoformat(last_backup_time)
    
    if source_dirs and backup_dest:
        create_backup(source_dirs, backup_dest, incremental, last_backup_time, group_name)
        backup_info[group_name] = datetime.datetime.now().isoformat()
        save_last_backup("last_backup.json", backup_info)
    else:
        log_backup("Invalid configuration for backup.")
