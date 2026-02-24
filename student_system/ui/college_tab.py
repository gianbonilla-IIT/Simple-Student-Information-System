"""
college_tab.py
UI tab for College CRUDL operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from core import college as repo
from ui.table_widget import TableWidget

COLUMNS = ["name", "code"]


class CollegeTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._build()

    def _build(self):
        # Table (left/top)
        self.table = TableWidget(
            self, columns=COLUMNS,
            load_fn=repo.list_all,
            on_select=self._on_row_select,
            bg=self["bg"],
        )
        self.table.pack(fill="both", expand=True)

        # Form (bottom)
        form_frame = ttk.LabelFrame(self, text="College Details", padding=10)
        form_frame.pack(fill="x", padx=8, pady=(0, 8))

        labels = ["Name", "Code"]
        self._vars = {
            "name": tk.StringVar(),
            "code": tk.StringVar(),
        }
        keys = list(self._vars.keys())

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", padx=4)
        ttk.Entry(form_frame, textvariable=self._vars["name"], width=35).grid(
            row=0, column=1, sticky="w", padx=4
        )

        tk.Label(form_frame, text="Code:").grid(row=0, column=2, sticky="e", padx=4)
        ttk.Entry(form_frame, textvariable=self._vars["code"], width=20).grid(
            row=0, column=3, sticky="w", padx=4
        )

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=8, pady=(0, 8))

        actions = [
            ("➕ Add", self._add),
            ("✏️ Update", self._update),
            ("🗑️ Delete", self._delete),
            ("🔄 Clear", self._clear),
        ]
        for text, cmd in actions:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side="left", padx=4)

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
            repo.create(d["code"], d["name"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"College '{d['code']}' added.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        d = self._get_form()
        try:
            repo.update(d["code"], d["name"])
            self.table.refresh()
            messagebox.showinfo("Success", f"College '{d['code']}' updated.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        d = self._get_form()
        if not d["code"]:
            messagebox.showwarning("Warning", "Select a college first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete college '{d['code']}'?"):
            return
        try:
            repo.delete(d["code"])
            self.table.refresh()
            self._clear()
            messagebox.showinfo("Success", f"College '{d['code']}' deleted.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
