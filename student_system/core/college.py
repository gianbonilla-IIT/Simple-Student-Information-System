"""
college.py
CRUD + List operations for College records.

CSV fields: code, name
"""

from core.csv_manager import read_csv, write_csv

FILEPATH = "data/colleges.csv"
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


def update(code: str, name: str) -> dict:
    """Update college name. Raises ValueError if not found."""
    code, name = code.strip().upper(), name.strip()
    _validate(code, name)
    rows = _load()
    for r in rows:
        if r["code"] == code:
            r["name"] = name
            _save(rows)
            return r
    raise ValueError(f"College '{code}' not found.")


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
