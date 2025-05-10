# utils/logger.py
import datetime

def log_event(event):
    with open("log.txt", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {event}\n")
