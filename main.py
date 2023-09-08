import json
import os
from datetime import datetime
import time
import glob
from concurrent.futures import ThreadPoolExecutor

FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'HEIC', 'mp4', 'MOV', 'JPG', 'PNG', 'MP4', 'mov']
DIRECTORY_PATH = r"YOUR PATH HERE"

def custom_str_to_unix_timestamp(date_str):
    # Converting custom date string to datetime object
    dt_object = datetime.strptime(date_str, '%b %d, %Y, %I:%M:%S %p %Z')

    # Convert datetime object to Unix timestamp
    unix_timestamp = time.mktime(dt_object.timetuple())

    return unix_timestamp

def process_file_pair(json_file, media_file):
    print(json_file)
    print(media_file)
    with open(json_file, 'r') as f:
        data = json.load(f)
        date = data['photoTakenTime']['formatted']
        date = custom_str_to_unix_timestamp(date)
    os.utime(media_file, (date, date))

def scan_directory(directory_path):
    files = []
    if os.path.isdir(directory_path):
        print(f"Directory {directory_path} exists.")
    else:
        print(f"Directory {directory_path} does not exist.")
        return
    for ext in FILE_EXTENSIONS:
        media_files = glob.glob(f"{directory_path}/**/*.{ext}", recursive=True)
        for media_file in media_files:
            json_file = f"{media_file}.json"
            if os.path.exists(json_file):
                process_file_pair(json_file, media_file)

scan_directory(DIRECTORY_PATH)
