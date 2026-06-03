"""
program_tab.py
UI tab for Program CRUDL operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core import program as repo
from core import college as college_repo
from ui.table_widget import TableWidget

COLUMNS = ["name", "code", "college"]


class ProgramTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._original_code = None  # Track the original code when a row is selected
        self._build()

    def _build(self):
        self.table = TableWidget(
            self, columns=COLUMNS,
            load_fn=repo.list_all,
            on_select=self._on_row_select,
            bg=self["bg"],
        )
        self.table.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(self, text="Program Details", padding=10)
        form_frame.pack(fill="x", padx=8, pady=(0, 8))

        self._vars = {
            "code": tk.StringVar(),
            "name": tk.StringVar(),
            "college": tk.StringVar(),
        }

        # Name
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", padx=4)
        ttk.Entry(form_frame, textvariable=self._vars["name"], width=35).grid(
        row=0, column=1, sticky="w", padx=4
        )

        # Code
        tk.Label(form_frame, text="Code:").grid(row=0, column=2, sticky="e", padx=4)
        ttk.Entry(form_frame, textvariable=self._vars["code"], width=20).grid(
        row=0, column=3, sticky="w", padx=4
        )

        # College dropdown
        tk.Label(form_frame, text="College:").grid(row=0, column=4, sticky="e", padx=4)
        self._college_combo = ttk.Combobox(
            form_frame, textvariable=self._vars["college"], width=12, state="readonly"
        )
        self._college_combo.grid(row=0, column=5, sticky="w", padx=4)
        self._refresh_college_options()

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=8, pady=(0, 8))

        actions = [
            ("➕ Add", self._add),
            ("✏️ Update", self._update),
            ("🗑️ Delete", self._delete),
            ("🔄 Clear", self._clear),
            ("↺ Refresh Colleges", self._refresh_college_options),
        ]
        for text, cmd in actions:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side="left", padx=4)

    def _refresh_college_options(self):
        colleges = college_repo.list_all()
        codes = [c["code"] for c in colleges]
        self._college_combo["values"] = codes

    def _on_row_select(self, row: dict):
        self._original_code = row.get("code", "")  # Store original code
        for key, var in self._vars.items():
            var.set(row.get(key, ""))

    def _get_form(self):
        return {k: v.get() for k, v in self._vars.items()}

    def _clear(self):
        self._original_code = None
        for var in self._vars.values():
            var.set("")

    def _add(self):
        d = self._get_form()
        try:
            repo.create(d["code"], d["name"], d["college"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"Program '{d['code']}' added.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        d = self._get_form()
        if not self._original_code:
            messagebox.showwarning("Warning", "Select a program first.")
            return
        try:
            repo.update(self._original_code, d["code"], d["name"], d["college"])
            self.table.refresh()
            self._original_code = d["code"]  # Update tracking after successful update
            messagebox.showinfo("Success", f"Program '{d['code']}' updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        d = self._get_form()
        if not d["code"]:
            messagebox.showwarning("Warning", "Select a program first.")
            return
        msg = f"Delete program '{d['code']}'?\n\nWarning: All students under this program will have their program set to NULL."
        if not messagebox.askyesno("Confirm Delete", msg):
            return
        try:
            repo.delete(d["code"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"Program '{d['code']}' deleted.\nAll related students have been updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        """Refresh both table and college options."""
        self._refresh_college_options()
        self.table.refresh()
