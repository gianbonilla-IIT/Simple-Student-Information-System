"""
table_widget.py
A reusable sortable, searchable Treeview table component.
"""

import tkinter as tk
from tkinter import ttk


class TableWidget(tk.Frame):
    """
    A self-contained table with:
    - Column header click-to-sort
    - Search bar
    - Scrollbars
    """

    def __init__(self, parent, columns: list[str], load_fn, on_select=None, **kwargs):
        """
        columns   : list of column names (also used as CSV field keys)
        load_fn   : callable(sort_by, reverse, search) -> list[dict]
        on_select : optional callback(selected_row_dict)
        """
        super().__init__(parent, **kwargs)
        self.columns = columns
        self.load_fn = load_fn
        self.on_select = on_select
        self._sort_col = columns[0]
        self._sort_rev = False

        self._build()
        self.refresh()

    def _build(self):
        # Search bar
        search_frame = tk.Frame(self, bg=self["bg"])
        search_frame.pack(fill="x", padx=8, pady=(8, 4))

        tk.Label(search_frame, text="🔍 Search:", bg=self["bg"],
                 font=("Segoe UI", 10)).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        entry = ttk.Entry(search_frame, textvariable=self._search_var, width=30)
        entry.pack(side="left", padx=6)

        btn = ttk.Button(search_frame, text="Clear", command=self._clear_search)
        btn.pack(side="left")

        # Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=self.columns,
            show="headings",
            selectmode="browse",
        )

        for col in self.columns:
            self.tree.heading(
                col, text=col.capitalize(),
                command=lambda c=col: self._sort(c),
            )
            self.tree.column(col, anchor="w", minwidth=80, width=140)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _clear_search(self):
        self._search_var.set("")

    def _sort(self, col: str):
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self.refresh()

    def refresh(self):
        """Reload data from load_fn and repopulate the table."""
        search = self._search_var.get().strip()
        try:
            rows = self.load_fn(
                sort_by=self._sort_col,
                reverse=self._sort_rev,
                search=search,
            )
        except Exception as e:
            rows = []
            print(f"[TableWidget] load error: {e}")

        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            values = [row.get(c, "") for c in self.columns]
            self.tree.insert("", "end", values=values)

        # Update sort arrow indicators
        for col in self.columns:
            arrow = ""
            if col == self._sort_col:
                arrow = " ▲" if not self._sort_rev else " ▼"
            self.tree.heading(col, text=col.capitalize() + arrow)

    def get_selected(self) -> dict | None:
        """Return the currently selected row as a dict, or None."""
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return dict(zip(self.columns, values))

    def _on_select(self, _event):
        if self.on_select:
            row = self.get_selected()
            if row:
                self.on_select(row)
