import os
from datetime import datetime
from collections import Counter

VALID_LOG_LEVELS = {"INFO", "WARNING", "ERROR", "DEBUG"}


def is_valid_log_level(level):
    """Check if log level is valid."""
    return level in VALID_LOG_LEVELS


def parse_log_line(line, line_number):
    """
    Parse a single log line into (timestamp, level, message).
    Returns None if line is invalid.
    """
    line = line.strip()

    if not line:
        return None

    try:
        parts = line.split(" ", 3)
        if len(parts) < 4:
            raise ValueError("Malformed log entry")

        date_part, time_part, log_level, message = parts

        if not is_valid_log_level(log_level):
            raise ValueError("Invalid log level")

        timestamp = datetime.strptime(
            f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S"
        )

        return (timestamp, log_level, message)

    except Exception:
        print(f"Warning: Skipping malformed line {line_number}: {line}")
        return None


def read_and_parse_logs(filename):
    """
    Reads log file and returns a list of parsed log tuples.
    """
    logs = []

    if not os.path.exists(filename):
        print("Error: logs.txt file not found.")
        return logs

    if os.stat(filename).st_size == 0:
        print("Log file is empty.")
        return logs

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            parsed_log = parse_log_line(line, line_number)
            if parsed_log:
                logs.append(parsed_log)

    return logs


def count_log_levels(logs):
    """Count occurrences of each log level."""
    return Counter(log[1] for log in logs)


def find_most_recent_log(logs, level):
    """Find most recent log entry for given level."""
    filtered_logs = [log for log in logs if log[1] == level]

    if not filtered_logs:
        return None

    return max(filtered_logs, key=lambda x: x[0])


def filter_logs_by_date(logs, start_date, end_date):
    """Filter logs within a date range."""
    return [log for log in logs if start_date <= log[0].date() <= end_date]


def save_filtered_logs(filtered_logs, filename):
    """Save filtered logs to file."""
    with open(filename, "w") as file:
        for log in filtered_logs:
            timestamp_str = log[0].strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp_str} {log[1]} {log[2]}\n")


def main():
    log_file = "logs.txt"
    output_file = "filtered_logs.txt"

    logs = read_and_parse_logs(log_file)

    if not logs:
        print("No valid logs to process.")
        return

    # ----- USER INPUT -----
    user_level = input("Enter log level (INFO/WARNING/ERROR/DEBUG): ").upper()

    if user_level not in VALID_LOG_LEVELS:
        print("Invalid log level entered.")
        return

    try:
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # ----- LOG LEVEL COUNTS -----
    print("\nLog Level Counts:")
    counts = count_log_levels(logs)
    for level in ["INFO", "WARNING", "ERROR", "DEBUG"]:
        print(f"{level}: {counts.get(level, 0)}")

    # ----- MOST RECENT ENTRY -----
    recent_log = find_most_recent_log(logs, user_level)

    if recent_log:
        timestamp_str = recent_log[0].strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nMost Recent {user_level} Entry:")
        print(f"{timestamp_str} {recent_log[1]} {recent_log[2]}")
    else:
        print(f"No logs found for level {user_level}")

    # ----- FILTER BY DATE RANGE -----
    filtered_logs = filter_logs_by_date(logs, start_date, end_date)

    if not filtered_logs:
        print("No logs found in the given date range.")
    else:
        save_filtered_logs(filtered_logs, output_file)
        print(f"\nFiltered Logs (Saved to {output_file}):")
        for log in filtered_logs:
            timestamp_str = log[0].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{timestamp_str} {log[1]} {log[2]}")


if __name__ == "__main__":
    main()
