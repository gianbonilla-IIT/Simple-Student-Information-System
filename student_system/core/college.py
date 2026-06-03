"""
college.py
CRUD + List operations for College records.

CSV fields: code, name
"""

from pathlib import Path
from core.csv_manager import read_csv, write_csv

FILEPATH = str(Path(__file__).parent.parent / "data" / "colleges.csv")
FIELDNAMES = ["code", "name"]


def _load() -> list[dict]:
    return read_csv(FILEPATH)


def _save(rows: list[dict]) -> None:
    write_csv(FILEPATH, FIELDNAMES, rows)


# ---------- Validation ----------

def _validate(code: str, name: str) -> None:
    if not code or not code.strip():
        raise ValueError("College code cannot be empty.")
    if not name or not name.strip():
        raise ValueError("College name cannot be empty.")
    if len(code.strip()) > 20:
        raise ValueError("College code must be 20 characters or fewer.")


# ---------- CRUDL ----------

def create(code: str, name: str) -> dict:
    """Create a new college. Raises ValueError on duplicate code."""
    code, name = code.strip().upper(), name.strip()
    _validate(code, name)
    rows = _load()
    if any(r["code"] == code for r in rows):
        raise ValueError(f"College code '{code}' already exists.")
    new_row = {"code": code, "name": name}
    rows.append(new_row)
    _save(rows)
    return new_row


def read(code: str) -> dict | None:
    """Return college by code, or None if not found."""
    code = code.strip().upper()
    for r in _load():
        if r["code"] == code:
            return r
    return None


def update(old_code: str, new_code: str, name: str) -> dict:
    """Update college code and/or name. Cascades code changes to programs. Raises ValueError if not found."""
    old_code, new_code, name = old_code.strip().upper(), new_code.strip().upper(), name.strip()
    _validate(new_code, name)
    rows = _load()
    
    # Find the college to update
    college_idx = None
    for i, r in enumerate(rows):
        if r["code"] == old_code:
            college_idx = i
            break
    
    if college_idx is None:
        raise ValueError(f"College '{old_code}' not found.")
    
    # Check if new code already exists (only if code is changing)
    if old_code != new_code:
        if any(r["code"] == new_code for r in rows):
            raise ValueError(f"College code '{new_code}' already exists.")
        # Cascade update to programs
        from core import program as prog_repo
        prog_repo._update_college_code(old_code, new_code)
    
    # Update the college
    rows[college_idx]["code"] = new_code
    rows[college_idx]["name"] = name
    _save(rows)
    return rows[college_idx]


def delete(code: str) -> None:
    """Delete a college. Raises ValueError if not found or referenced by programs."""
    from core import program as prog_repo  # avoid circular at module level
    code = code.strip().upper()
    rows = _load()
    found = any(r["code"] == code for r in rows)
    if not found:
        raise ValueError(f"College '{code}' not found.")
    # Referential integrity check
    programs = prog_repo.list_all()
    if any(p["college"] == code for p in programs):
        raise ValueError(
            f"Cannot delete college '{code}': it is referenced by one or more programs."
        )
    rows = [r for r in rows if r["code"] != code]
    _save(rows)


def list_all(sort_by: str = "code", reverse: bool = False,
             search: str = "") -> list[dict]:
    """List colleges with optional sort and search."""
    rows = _load()
    if search:
        s = search.lower()
        rows = [r for r in rows if s in r["code"].lower() or s in r["name"].lower()]
    valid_sort = {"code", "name"}
    if sort_by not in valid_sort:
        sort_by = "code"
    rows.sort(key=lambda r: r[sort_by].lower(), reverse=reverse)
    return rows
