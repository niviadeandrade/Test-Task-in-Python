import os
import shutil
import time
import hashlib

def verify_folder (file_path):
  hash = hashlib.md5()
  with open (file_path, "rb") as fl:
    
