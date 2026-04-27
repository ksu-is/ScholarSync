import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime


DB_NAME = "scholarsync.db"



# DATABASE FUNCTIONS
# These functions create and connect to the SQLite database.
# The database file will be created automatically when the app runs.

def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    """Creates the tables needed for ScholarSync if they do not already exist."""
    conn = connect_db()
    cursor = conn.cursor()

    # Assignment table stores class assignments and due dates.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course TEXT,
            due_date TEXT,
            status TEXT,
            priority TEXT
        )
    """)
    # Task table stores simple daily to-do items.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    # Notes table stores quick notes with the date and time they were created.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
      
    # MAIN LAYOUT
    
    def setup_ui(self):
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh", command=self.refresh_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Header/banner area.
        header = tk.Frame(self.root, bg="#ff8fab", height=95)
        header.pack(fill="x")

        title = ttk.Label(header, text="ScholarSync", style="Title.TLabel")
        title.pack(pady=(15, 0))

        subtitle = ttk.Label(header, text="A cute student planner for assignments, tasks, notes, and focus time", style="SubTitle.TLabel")
        subtitle.pack()

        # Main notebook/tabs.
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        self.dashboard_frame = tk.Frame(self.notebook, bg="#fff7fb")
        self.assignment_frame = tk.Frame(self.notebook, bg="#fff7fb")
        self.todo_frame = tk.Frame(self.notebook, bg="#fff7fb")
        self.notes_frame = tk.Frame(self.notebook, bg="#fff7fb")
        self.timer_frame = tk.Frame(self.notebook, bg="#fff7fb")

        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.assignment_frame, text="Assignments")
        self.notebook.add(self.todo_frame, text="To-Do List")
        self.notebook.add(self.notes_frame, text="Notes")
        self.notebook.add(self.timer_frame, text="Study Timer")

        self.build_dashboard_tab()
        self.build_assignment_tab()
        self.build_todo_tab()
        self.build_notes_tab()
        self.build_timer_tab()
        
          # Status bar
        self.status_bar = tk.Label(self.root, text="", anchor="w", bg="#fce4ec", fg="#4a3f55", font=("Segoe UI", 10))
        self.status_bar.pack(side="bottom", fill="x")
        
        