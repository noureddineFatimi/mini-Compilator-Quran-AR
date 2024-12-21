import datetime

def log_error(error_message):
    with open("analyzer/error_logs.txt", "a",encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {error_message}\n")