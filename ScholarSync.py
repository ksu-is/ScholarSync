import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime


DB_NAME = "scholarsync.db"


# ============================================================
# DATABASE FUNCTIONS
# These functions create and connect to the SQLite database.
# The database file will be created automatically when the app runs.
# ============================================================
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
    