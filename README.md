# Server Log Analyzer

## Overview
This project is a Python program that analyzes server log files.  
It reads a log file, counts log levels, finds the most recent log entry for a given level, filters logs by date range, and saves the filtered logs to a new file.

---

## Project Structure
log.py
log_analyser.txt
filtered_logs.txt
test_log_analyser.py
README.md

---

## Requirements
- Python 3.x
- pytest (optional, for unit tests)

Install pytest:pip install pytest


---

## How to Run the Program

1. Place `log_analyser.txt` in the same folder as `log.py`
2. Run the script:python log.py
3. Enter inputs when prompted:
Enter log level (INFO/WARNING/ERROR/DEBUG): ERROR
Enter start date (YYYY-MM-DD): 2025-01-10
Enter end date (YYYY-MM-DD): 2025-01-10


---

## Sample Input (logs.txt)
2025-01-10 09:23:45 INFO Application started
2025-01-10 09:25:00 WARNING Disk space low
2025-01-10 09:26:30 ERROR Unable to connect to database
2025-01-10 09:30:15 INFO User logged in
2025-01-10 09:35:20 ERROR Timeout occurred
2025-01-10 09:40:05 WARNING CPU usage high
2025-01-11 10:15:45 DEBUG Debugging started


---

## Expected Output
Log Level Counts:
INFO: 2
WARNING: 2
ERROR: 2
DEBUG: 1

Most Recent ERROR Entry:
2025-01-10 09:35:20 ERROR Timeout occurred

Filtered Logs (Saved to filtered_logs.txt):
2025-01-10 09:23:45 INFO Application started
2025-01-10 09:25:00 WARNING Disk space low
2025-01-10 09:26:30 ERROR Unable to connect to database
2025-01-10 09:30:15 INFO User logged in
2025-01-10 09:35:20 ERROR Timeout occurred
2025-01-10 09:40:05 WARNING CPU usage high


---

##  Error Handling
The program handles:
- Empty log file
- Invalid log format
- Invalid log levels
- Invalid date format
- No logs found in date range

---

##  Assumptions
- Log file format is:  
  `<timestamp> <log_level> <message>`
- Valid log levels are: INFO, WARNING, ERROR, DEBUG
- Date format is YYYY-MM-DD

---

## Run Unit Tests (Optional)

Run tests using pytest: pytest


---

##  Submission
This project contains:
- log.py
- log_analyser.txt
- filtered_logs.txt
- README.md
- test_log_analyser.py
