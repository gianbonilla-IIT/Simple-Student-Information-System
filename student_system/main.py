"""
main.py
Entry point for the Student Information System.
Run with:  python main.py
"""

import tkinter as tk
from tkinter import ttk

from ui.college_tab import CollegeTab
from ui.program_tab import ProgramTab
from ui.student_tab import StudentTab


def main():
    root = tk.Tk()
    root.title("Student Information System")
    root.geometry("900x620")
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (900 // 2)
    y = (root.winfo_screenheight() // 2) - (620 // 2)
    root.geometry(f"900x620+{x}+{y}")
    root.minsize(750, 520)

    # Style
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 5])
    style.configure("TFrame", background="#f0f4f8")
    style.configure("TLabelframe", background="#f0f4f8")
    style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"), background="#f0f4f8")
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    # Header
    header = tk.Frame(root, bg="#1a3a5c", height=50)
    header.pack(fill="x")
    tk.Label(
        header, text="📚  Student Information System",
        bg="#1a3a5c", fg="white",
        font=("Segoe UI", 14, "bold"), pady=10
    ).pack(side="left", padx=16)

    # Tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    bg = "#f0f4f8"

    college_tab = CollegeTab(notebook, bg=bg)
    program_tab = ProgramTab(notebook, bg=bg)
    student_tab = StudentTab(notebook, bg=bg)

    notebook.add(college_tab, text="🏫  Colleges")
    notebook.add(program_tab, text="📋  Programs")
    notebook.add(student_tab, text="🎓  Students")

    root.mainloop()


if __name__ == "__main__":
    main()
