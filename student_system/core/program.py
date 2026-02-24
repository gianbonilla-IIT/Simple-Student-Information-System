"""
program.py
CRUD + List operations for Program records.

CSV fields: code, name, college
"""

from core.csv_manager import read_csv, write_csv

FILEPATH = "data/programs.csv"
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


def update(code: str, name: str, college_code: str) -> dict:
    from core import college as col_repo
    code, name, college_code = code.strip().upper(), name.strip(), college_code.strip().upper()
    _validate(code, name, college_code)
    if col_repo.read(college_code) is None:
        raise ValueError(f"College '{college_code}' does not exist.")
    rows = _load()
    for r in rows:
        if r["code"] == code:
            r["name"] = name
            r["college"] = college_code
            _save(rows)
            return r
    raise ValueError(f"Program '{code}' not found.")


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
