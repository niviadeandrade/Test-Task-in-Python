import os
import shutil
import time
import hashlib
from datetime import datetime

def verify_folder (file_path):
  hash_folder = hashlib.md5()
  with open (file_path, "rb") as fl:
    for chunk in iter(lambda: fl.read(4096), b""):
      hash_folder.update(chunk)
  return hash_folder.hexdigest()

def creating_log_file():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"log_{timestamp}.txt"
    with open(log_file, 'w') as new_log:
        new_log.write("Log file created\n")
    return log_file

def sync_folder (source_folder, replica_folder, log_file):
  if log_file.strip() == "":
     log_file = creating_log_file()

  if not os.path.exists(log_file):
        with open(log_file, 'w') as new_log:
            new_log.write("Log file created\n")

  for root, dirs, files in os.walk(source_folder):
    replica_root = root.replace(source_folder, replica_folder, 1)

    for directory in dirs:
      source_dir = os.path.join(root, directory)
      replica_dir = source_dir.replace(source_folder, replica_folder, 1)
      if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)

    for file in files:
      source_file = os.path.join(root, file)
      replica_file = source_file.replace(source_folder, replica_folder, 1)

      if not os.path.exists(replica_file) or verify_folder(replica_file) != verify_folder(source_file):
        shutil.copy2(source_file, replica_file)
        print("Copied", source_file, "to", replica_file)
        with open(log_file, 'a') as log:
          log.write(f"Copied {source_file} to {replica_file} \n")

    for replica_root, replica_dirs_, replica_file in os.walk(replica_folder):
        source_root = replica_root.replace(replica_folder, source_folder, 1)

        for replica_file in replica_file:
            source_file = os.path.join(source_root, replica_file)
            replica_file = os.path.join(replica_root, replica_file)
            if not os.path.exists(source_file):
               os.remove(replica_file)
               print("Removed", replica_file)
               with open(log_file, 'a') as log:
                   log.write("Removed", replica_file, "\n")

if __name__ == "__main__":
  source_folder = input("Enter a source folder path: ")
  replica_folder = input("Enter a replica folder path: ")
  log_file = input("Enter a log file path (if you don't have, leave blank to create a new one): ")
  interval = int(input("Enter the sync interval (in seconds): "))

  while True:
    sync_folder(source_folder, replica_folder, log_file)
    time.sleep(interval)

    
