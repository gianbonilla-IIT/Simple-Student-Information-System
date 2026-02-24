"""
student.py
CRUD + List operations for Student records.

CSV fields: id, firstname, lastname, program, year, gender
ID format: YYYY-NNNN  (e.g. 2024-0001)
"""

import re
from core.csv_manager import read_csv, write_csv

FILEPATH = "data/students.csv"
FIELDNAMES = ["id", "firstname", "lastname", "program", "year", "gender"]
ID_PATTERN = re.compile(r"^\d{4}-\d{4}$")
VALID_GENDERS = {"Male", "Female", "Other"}
VALID_YEARS = {"1", "2", "3", "4", "5"}


def _load() -> list[dict]:
    return read_csv(FILEPATH)


def _save(rows: list[dict]) -> None:
    write_csv(FILEPATH, FIELDNAMES, rows)


def _validate(student_id: str, firstname: str, lastname: str,
              program_code: str, year: str, gender: str) -> None:
    if not ID_PATTERN.match(student_id):
        raise ValueError("Student ID must follow YYYY-NNNN format (e.g. 2024-0001).")
    if not firstname or not firstname.strip():
        raise ValueError("First name cannot be empty.")
    if not lastname or not lastname.strip():
        raise ValueError("Last name cannot be empty.")
    if not program_code or not program_code.strip():
        raise ValueError("Program code cannot be empty.")
    if year not in VALID_YEARS:
        raise ValueError(f"Year must be one of: {', '.join(sorted(VALID_YEARS))}.")
    if gender not in VALID_GENDERS:
        raise ValueError(f"Gender must be one of: {', '.join(sorted(VALID_GENDERS))}.")


def create(student_id: str, firstname: str, lastname: str,
           program_code: str, year: str, gender: str) -> dict:
    from core import program as prog_repo
    student_id = student_id.strip()
    firstname, lastname = firstname.strip(), lastname.strip()
    program_code = program_code.strip().upper()
    year, gender = year.strip(), gender.strip()

    _validate(student_id, firstname, lastname, program_code, year, gender)
    if prog_repo.read(program_code) is None:
        raise ValueError(f"Program '{program_code}' does not exist.")
    rows = _load()
    if any(r["id"] == student_id for r in rows):
        raise ValueError(f"Student ID '{student_id}' already exists.")
    new_row = {
        "id": student_id, "firstname": firstname, "lastname": lastname,
        "program": program_code, "year": year, "gender": gender,
    }
    rows.append(new_row)
    _save(rows)
    return new_row


def read(student_id: str) -> dict | None:
    student_id = student_id.strip()
    for r in _load():
        if r["id"] == student_id:
            return r
    return None


def update(student_id: str, firstname: str, lastname: str,
           program_code: str, year: str, gender: str) -> dict:
    from core import program as prog_repo
    student_id = student_id.strip()
    firstname, lastname = firstname.strip(), lastname.strip()
    program_code = program_code.strip().upper()
    year, gender = year.strip(), gender.strip()

    _validate(student_id, firstname, lastname, program_code, year, gender)
    if prog_repo.read(program_code) is None:
        raise ValueError(f"Program '{program_code}' does not exist.")
    rows = _load()
    for r in rows:
        if r["id"] == student_id:
            r["firstname"] = firstname
            r["lastname"] = lastname
            r["program"] = program_code
            r["year"] = year
            r["gender"] = gender
            _save(rows)
            return r
    raise ValueError(f"Student '{student_id}' not found.")


def delete(student_id: str) -> None:
    student_id = student_id.strip()
    rows = _load()
    if not any(r["id"] == student_id for r in rows):
        raise ValueError(f"Student '{student_id}' not found.")
    rows = [r for r in rows if r["id"] != student_id]
    _save(rows)


def list_all(sort_by: str = "id", reverse: bool = False,
             search: str = "") -> list[dict]:
    rows = _load()
    if search:
        s = search.lower()
        rows = [
            r for r in rows
            if any(s in r[field].lower() for field in FIELDNAMES)
        ]
    valid_sort = set(FIELDNAMES)
    if sort_by not in valid_sort:
        sort_by = "id"
    rows.sort(key=lambda r: r[sort_by].lower(), reverse=reverse)
    return rows
