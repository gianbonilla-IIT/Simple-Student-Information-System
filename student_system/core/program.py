"""
program.py
CRUD + List operations for Program records.

CSV fields: code, name, college
"""

from pathlib import Path
from core.csv_manager import read_csv, write_csv

FILEPATH = str(Path(__file__).parent.parent / "data" / "programs.csv")
FIELDNAMES = ["code", "name", "college"]


def _load() -> list[dict]:
    return read_csv(FILEPATH)


def _save(rows: list[dict]) -> None:
    write_csv(FILEPATH, FIELDNAMES, rows)


def _validate(code: str, name: str, college_code: str) -> None:
    if not code or not code.strip():
        raise ValueError("Program code cannot be empty.")
    if not name or not name.strip():
        raise ValueError("Program name cannot be empty.")
    if not college_code or not college_code.strip():
        raise ValueError("College code cannot be empty.")


def create(code: str, name: str, college_code: str) -> dict:
    from core import college as col_repo
    code, name, college_code = code.strip().upper(), name.strip(), college_code.strip().upper()
    _validate(code, name, college_code)
    if col_repo.read(college_code) is None:
        raise ValueError(f"College '{college_code}' does not exist.")
    rows = _load()
    if any(r["code"] == code for r in rows):
        raise ValueError(f"Program code '{code}' already exists.")
    new_row = {"code": code, "name": name, "college": college_code}
    rows.append(new_row)
    _save(rows)
    return new_row


def read(code: str) -> dict | None:
    code = code.strip().upper()
    for r in _load():
        if r["code"] == code:
            return r
    return None


def update(old_code: str, new_code: str, name: str, college_code: str) -> dict:
    """Update program code and/or details. Cascades code changes to students. Raises ValueError if not found."""
    from core import college as col_repo
    old_code, new_code, name = old_code.strip().upper(), new_code.strip().upper(), name.strip()
    college_code = college_code.strip().upper()
    _validate(new_code, name, college_code)
    
    if col_repo.read(college_code) is None:
        raise ValueError(f"College '{college_code}' does not exist.")
    
    rows = _load()
    
    # Find the program to update
    program_idx = None
    for i, r in enumerate(rows):
        if r["code"] == old_code:
            program_idx = i
            break
    
    if program_idx is None:
        raise ValueError(f"Program '{old_code}' not found.")
    
    # Check if new code already exists (only if code is changing)
    if old_code != new_code:
        if any(r["code"] == new_code for r in rows):
            raise ValueError(f"Program code '{new_code}' already exists.")
        # Cascade update to students
        from core import student as stu_repo
        stu_repo._update_program_code(old_code, new_code)
    
    # Update the program
    rows[program_idx]["code"] = new_code
    rows[program_idx]["name"] = name
    rows[program_idx]["college"] = college_code
    _save(rows)
    return rows[program_idx]


def _update_college_code(old_college_code: str, new_college_code: str) -> None:
    """Internal function to cascade college code changes to programs."""
    rows = _load()
    for r in rows:
        if r["college"] == old_college_code:
            r["college"] = new_college_code
    _save(rows)


def delete(code: str) -> None:
    from core import student as stu_repo
    code = code.strip().upper()
    rows = _load()
    if not any(r["code"] == code for r in rows):
        raise ValueError(f"Program '{code}' not found.")
    students = stu_repo.list_all()
    if any(s["program"] == code for s in students):
        raise ValueError(
            f"Cannot delete program '{code}': it is referenced by one or more students."
        )
    rows = [r for r in rows if r["code"] != code]
    _save(rows)


def list_all(sort_by: str = "code", reverse: bool = False,
             search: str = "") -> list[dict]:
    rows = _load()
    if search:
        s = search.lower()
        rows = [
            r for r in rows
            if s in r["code"].lower() or s in r["name"].lower() or s in r["college"].lower()
        ]
    valid_sort = {"code", "name", "college"}
    if sort_by not in valid_sort:
        sort_by = "code"
    rows.sort(key=lambda r: r[sort_by].lower(), reverse=reverse)
    return rows
