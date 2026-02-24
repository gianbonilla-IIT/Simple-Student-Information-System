"""
csv_manager.py
Low-level CSV read/write with atomic (ACID-like) operations via temp-file + replace.
"""

import csv
import os
import shutil
import tempfile
import threading
from pathlib import Path

# One lock per file path to allow concurrent access to different files
_locks: dict[str, threading.Lock] = {}
_locks_lock = threading.Lock()


def _get_lock(filepath: str) -> threading.Lock:
    with _locks_lock:
        if filepath not in _locks:
            _locks[filepath] = threading.Lock()
        return _locks[filepath]


def read_csv(filepath: str) -> list[dict]:
    """Read all rows from a CSV file. Returns list of dicts."""
    path = Path(filepath)
    if not path.exists():
        return []
    lock = _get_lock(filepath)
    with lock:
        try:
            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader]
        except Exception as e:
            raise IOError(f"Failed to read '{filepath}': {e}")


def write_csv(filepath: str, fieldnames: list[str], rows: list[dict]) -> None:
    """
    Atomically write rows to a CSV file.
    Uses write-to-temp + atomic rename to prevent data corruption.
    """
    lock = _get_lock(filepath)
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with lock:
        try:
            # Write to a temp file in the same directory
            dir_ = path.parent
            fd, tmp_path = tempfile.mkstemp(dir=dir_, suffix=".tmp")
            try:
                with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                # Atomic replace
                shutil.move(tmp_path, filepath)
            except Exception:
                os.unlink(tmp_path)
                raise
        except Exception as e:
            raise IOError(f"Failed to write '{filepath}': {e}")
