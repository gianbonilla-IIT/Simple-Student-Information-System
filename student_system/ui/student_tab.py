"""
student_tab.py
UI tab for Student CRUDL operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core import student as repo
from core import program as program_repo
from ui.table_widget import TableWidget

COLUMNS = ["id", "firstname", "lastname", "program", "year", "gender"]


class StudentTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._build()

    def _build(self):
        self.table = TableWidget(
            self, columns=COLUMNS,
            load_fn=repo.list_all,
            on_select=self._on_row_select,
            bg=self["bg"],
        )
        self.table.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(self, text="Student Details", padding=10)
        form_frame.pack(fill="x", padx=8, pady=(0, 8))

        self._vars = {
            "id": tk.StringVar(),
            "firstname": tk.StringVar(),
            "lastname": tk.StringVar(),
            "program": tk.StringVar(),
            "year": tk.StringVar(),
            "gender": tk.StringVar(),
        }

        # Row 0
        fields_r0 = [
            ("ID (YYYY-NNNN)", "id", None),
            ("First Name", "firstname", None),
            ("Last Name", "lastname", None),
        ]
        for col, (lbl, key, _) in enumerate(fields_r0):
            tk.Label(form_frame, text=lbl + ":").grid(row=0, column=col * 2, sticky="e", padx=4, pady=3)
            ttk.Entry(form_frame, textvariable=self._vars[key], width=18).grid(
                row=0, column=col * 2 + 1, sticky="w", padx=4
            )

        # Row 1 - Program (combo), Year (combo), Gender (combo)
        tk.Label(form_frame, text="Program:").grid(row=1, column=0, sticky="e", padx=4, pady=3)
        self._prog_combo = ttk.Combobox(
            form_frame, textvariable=self._vars["program"], width=16, state="normal"
        )
        self._prog_combo.grid(row=1, column=1, sticky="w", padx=4)
        self._refresh_program_options()

        tk.Label(form_frame, text="Year:").grid(row=1, column=2, sticky="e", padx=4)
        ttk.Combobox(
            form_frame, textvariable=self._vars["year"],
            values=["1", "2", "3", "4", "5"], width=5, state="readonly"
        ).grid(row=1, column=3, sticky="w", padx=4)

        tk.Label(form_frame, text="Gender:").grid(row=1, column=4, sticky="e", padx=4)
        ttk.Combobox(
            form_frame, textvariable=self._vars["gender"],
            values=["Male", "Female", "Other"], width=10, state="readonly"
        ).grid(row=1, column=5, sticky="w", padx=4)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=8, pady=(0, 8))

        actions = [
            ("➕ Add", self._add),
            ("✏️ Update", self._update),
            ("🗑️ Delete", self._delete),
            ("🔄 Clear", self._clear),
            ("↺ Refresh Programs", self._refresh_program_options),
        ]
        for text, cmd in actions:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side="left", padx=4)

    def _refresh_program_options(self):
        programs = program_repo.list_all()
        codes = [p["code"] for p in programs]
        self._prog_combo["values"] = codes

    def _on_row_select(self, row: dict):
        for key, var in self._vars.items():
            var.set(row.get(key, ""))

    def _get_form(self):
        return {k: v.get() for k, v in self._vars.items()}

    def _clear(self):
        for var in self._vars.values():
            var.set("")

    def _add(self):
        d = self._get_form()
        try:
            repo.create(d["id"], d["firstname"], d["lastname"],
                        d["program"], d["year"], d["gender"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"Student '{d['id']}' added.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        d = self._get_form()
        try:
            repo.update(d["id"], d["firstname"], d["lastname"],
                        d["program"], d["year"], d["gender"])
            self.table.refresh()
            messagebox.showinfo("Success", f"Student '{d['id']}' updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        d = self._get_form()
        if not d["id"]:
            messagebox.showwarning("Warning", "Select a student first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete student '{d['id']}'?"):
            return
        try:
            repo.delete(d["id"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"Student '{d['id']}' deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
