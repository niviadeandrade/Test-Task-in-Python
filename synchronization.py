import os
import shutil
import time
import hashlib

def verify_folder (file_path):
  hash_folder = hashlib.md5()
  with open (file_path, "rb") as fl:
    for chunk in iter(lambda: fl.read(4096), b""):
      hash_folder.update(chunk)
  return hash_folder.hexdigest()




    
