import os
from datetime import datetime
import pytest

from log_analyzer import (
    read_and_parse_logs,
    count_log_levels,
    find_most_recent_log,
    filter_logs_by_date
)

# FIXTURE: sample log file
@pytest.fixture
def sample_log_file(tmp_path):
    file_path = tmp_path / "logs.txt"
    file_path.write_text(
        "2025-01-10 09:23:45 INFO Application started\n"
        "2025-01-10 09:25:00 WARNING Disk space low\n"
        "2025-01-10 09:26:30 ERROR Unable to connect to database\n"
        "2025-01-10 09:30:15 INFO User logged in\n"
        "2025-01-10 09:35:20 ERROR Timeout occurred\n"
        "2025-01-11 10:15:45 DEBUG Debugging started\n"
    )
    return file_path


# TEST: Read and parse logs
def test_read_and_parse_logs(sample_log_file):
    logs = read_and_parse_logs(sample_log_file)

    assert len(logs) == 6
    assert logs[0][1] == "INFO"
    assert logs[2][1] == "ERROR"
    assert logs[0][2] == "Application started"


# TEST: Count log levels 
def test_count_log_levels(sample_log_file):
    logs = read_and_parse_logs(sample_log_file)
    counts = count_log_levels(logs)

    assert counts["INFO"] == 2
    assert counts["WARNING"] == 1
    assert counts["ERROR"] == 2
    assert counts["DEBUG"] == 1


# TEST: Most recent ERROR log 
def test_find_most_recent_error(sample_log_file):
    logs = read_and_parse_logs(sample_log_file)
    recent_error = find_most_recent_log(logs, "ERROR")

    timestamp = recent_error[0].strftime("%Y-%m-%d %H:%M:%S")
    assert timestamp == "2025-01-10 09:35:20"
    assert recent_error[1] == "ERROR"


#  TEST: Filter logs by date 
def test_filter_logs_by_date(sample_log_file):
    logs = read_and_parse_logs(sample_log_file)

    start_date = datetime.strptime("2025-01-10", "%Y-%m-%d").date()
    end_date = datetime.strptime("2025-01-10", "%Y-%m-%d").date()

    filtered = filter_logs_by_date(logs, start_date, end_date)

    assert len(filtered) == 5  # only logs from Jan 10
    assert filtered[0][1] == "INFO"


# TEST: No logs in date range 
def test_no_logs_in_date_range(sample_log_file):
    logs = read_and_parse_logs(sample_log_file)

    start_date = datetime.strptime("2025-01-20", "%Y-%m-%d").date()
    end_date = datetime.strptime("2025-01-21", "%Y-%m-%d").date()

    filtered = filter_logs_by_date(logs, start_date, end_date)

    assert filtered == []


# TEST: Empty log file
def test_empty_log_file(tmp_path):
    empty_file = tmp_path / "empty_logs.txt"
    empty_file.write_text("")

    logs = read_and_parse_logs(empty_file)
    assert logs == []
