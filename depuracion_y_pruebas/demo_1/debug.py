import os

common_paths = [
    "/var/log",
    "/usr/local/log",
    "/etc/log"
]


def look_for_log_files():
    log_files = []
    for path in common_paths:
        try:
            for filename in os.listdir(path):
                if filename.endswith(".log"):
                    log_files.append(os.path.join(path, filename))
        except FileNotFoundError:
            print(f"Error: The path {path} does not exist.")
    return log_files
                
# Merge log files
logs = look_for_log_files()
print(logs)

def read_logs(logs):
    merged_logs = ""
    for log in logs:
        with open(log, "r") as f:
            merged_logs += f.read()
    return merged_logs


merged_logs = read_logs(logs)
print(merged_logs)