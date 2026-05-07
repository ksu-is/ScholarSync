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
        
          # DASHBOARD TAB
    
    def build_dashboard_tab(self):
        welcome = tk.Label(
            self.dashboard_frame,
            text="Welcome back! Let’s stay organized today ✨",
            font=("Segoe UI", 22, "bold"),
            bg="#fff7fb",
            fg="#4a3f55"
        )
        welcome.pack(pady=30)

        card_frame = tk.Frame(self.dashboard_frame, bg="#fff7fb")
        card_frame.pack(pady=20)

        self.assignment_count_label = self.create_dashboard_card(card_frame, "Assignments", "0", "Things due soon")
        self.task_count_label = self.create_dashboard_card(card_frame, "To-Do Tasks", "0", "Daily reminders")
        self.note_count_label = self.create_dashboard_card(card_frame, "Notes", "0", "Saved thoughts")

    def create_dashboard_card(self, parent, title, number, description):
        card = tk.Frame(parent, bg="white", padx=35, pady=25, highlightbackground="#ffd6e0", highlightthickness=2)
        card.pack(side="left", padx=15)

        tk.Label(card, text=title, font=("Segoe UI", 14, "bold"), bg="white", fg="#4a3f55").pack()
        number_label = tk.Label(card, text=number, font=("Segoe UI", 32, "bold"), bg="white", fg="#b388ff")
        number_label.pack(pady=5)
        tk.Label(card, text=description, font=("Segoe UI", 10), bg="white", fg="#777777").pack()
        return number_label
    
     # ASSIGNMENT TAB
     
    def build_assignment_tab(self):
        form = tk.LabelFrame(
            self.assignment_frame,
            text="Add Assignment",
            font=("Segoe UI", 11, "bold"),
            bg="#fff7fb",
            fg="#4a3f55",
            padx=15,
            pady=15
        )
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Title", bg="#fff7fb", fg="#4a3f55").grid(row=0, column=0, sticky="w")
        tk.Label(form, text="Course", bg="#fff7fb", fg="#4a3f55").grid(row=0, column=1, sticky="w")
        tk.Label(form, text="Due Date (YYYY-MM-DD)", bg="#fff7fb", fg="#4a3f55").grid(row=0, column=2, sticky="w")
        tk.Label(form, text="Priority", bg="#fff7fb", fg="#4a3f55").grid(row=0, column=3, sticky="w")

        self.assignment_title = tk.Entry(form, width=25)
        self.assignment_course = tk.Entry(form, width=20)
        self.assignment_due = tk.Entry(form, width=18)
        self.assignment_priority = ttk.Combobox(form, values=["Low", "Medium", "High"], width=12, state="readonly")
        self.assignment_priority.set("Medium")
        
        
        self.assignment_title.grid(row=1, column=0, padx=5, pady=5)
        self.assignment_course.grid(row=1, column=1, padx=5, pady=5)
        self.assignment_due.grid(row=1, column=2, padx=5, pady=5)
        self.assignment_priority.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form, text="Add", style="Cute.TButton", command=self.add_assignment).grid(row=1, column=4, padx=5)
        ttk.Button(form, text="Update Status", style="Cute.TButton", command=self.update_assignment_status).grid(row=1, column=5, padx=5)
        ttk.Button(form, text="Delete", style="Cute.TButton", command=self.delete_assignment).grid(row=1, column=6, padx=5)

        self.assignment_tree = ttk.Treeview(
            self.assignment_frame,
            columns=("ID", "Title", "Course", "Due Date", "Status", "Priority"),
            show="headings"
        )

        for column in ("ID", "Title", "Course", "Due Date", "Status", "Priority"):
            self.assignment_tree.heading(column, text=column)

        self.assignment_tree.column("ID", width=50)
        self.assignment_tree.column("Title", width=250)
        self.assignment_tree.column("Course", width=150)
        self.assignment_tree.column("Due Date", width=140)
        self.assignment_tree.column("Status", width=140)
        self.assignment_tree.column("Priority", width=100)
        self.assignment_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_assignment(self):
        title = self.assignment_title.get().strip()
        course = self.assignment_course.get().strip()
        due_date = self.assignment_due.get().strip()
        priority = self.assignment_priority.get()

        if not title:
            messagebox.showerror("Missing Information", "Please enter an assignment title.")
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Date Error", "Please use the date format YYYY-MM-DD.")
                return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO assignments (title, course, due_date, status, priority) VALUES (?, ?, ?, ?, ?)",
            (title, course, due_date, "Not Started", priority)
        )
        conn.commit()
        conn.close()
        
        self.assignment_title.delete(0, tk.END)
        self.assignment_course.delete(0, tk.END)
        self.assignment_due.delete(0, tk.END)
        self.assignment_priority.set("Medium")
        self.refresh_all()

    def load_assignments(self):
        for item in self.assignment_tree.get_children():
            self.assignment_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assignments ORDER BY due_date ASC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.assignment_tree.insert("", "end", values=row)

    def update_assignment_status(self):
        selected = self.assignment_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an assignment first.")
            return

        assignment_id = self.assignment_tree.item(selected[0])["values"][0]
        new_status = simpledialog.askstring(
            "Update Status",
            "Enter status: Not Started, In Progress, or Completed",
            initialvalue="In Progress"
        )

        if new_status is None:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE assignments SET status = ? WHERE id = ?", (new_status, assignment_id))
        conn.commit()
        conn.close()
        self.refresh_all()

    def delete_assignment(self):
        selected = self.assignment_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an assignment first.")
            return

        assignment_id = self.assignment_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this assignment?"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
            conn.commit()
            conn.close()
            self.refresh_all()
            
              # TO-DO TAB

    def build_todo_tab(self):
        frame = tk.LabelFrame(self.todo_frame, text="Daily To-Do List", font=("Segoe UI", 11, "bold"), bg="#fff7fb", fg="#4a3f55", padx=15, pady=15)
        frame.pack(fill="x", padx=10, pady=10)

        self.task_entry = tk.Entry(frame, width=70, font=("Segoe UI", 11))
        self.task_entry.pack(side="left", padx=5)

        ttk.Button(frame, text="Add Task", style="Cute.TButton", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(frame, text="Delete Task", style="Cute.TButton", command=self.delete_task).pack(side="left", padx=5)

        self.task_listbox = tk.Listbox(self.todo_frame, font=("Segoe UI", 12), height=20, bg="white", fg="#4a3f55", selectbackground="#b388ff")
        self.task_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showerror("Missing Task", "Please type a task.")
            return
        
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))
        conn.commit()
        conn.close()

        self.task_entry.delete(0, tk.END)
        self.refresh_all()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.task_listbox.insert(tk.END, f"{row[0]}. {row[1]}")
            
            conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.task_listbox.insert(tk.END, f"{row[0]}. {row[1]}")

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first.")
            return

        task_text = self.task_listbox.get(selected[0])
        task_id = task_text.split(".")[0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self.refresh_all()
        
          # NOTES TAB
   
    def build_notes_tab(self):
        note_frame = tk.LabelFrame(self.notes_frame, text="Quick Notes", font=("Segoe UI", 11, "bold"), bg="#fff7fb", fg="#4a3f55", padx=15, pady=15)
        note_frame.pack(fill="x", padx=10, pady=10)

        self.notes_text = tk.Text(note_frame, height=7, font=("Segoe UI", 11), wrap="word", bg="white", fg="#4a3f55")
        self.notes_text.pack(fill="x", pady=5)

        ttk.Button(note_frame, text="Save Note", style="Cute.TButton", command=self.save_note).pack(pady=5)

        self.notes_listbox = tk.Listbox(self.notes_frame, font=("Segoe UI", 11), height=15, bg="white", fg="#4a3f55", selectbackground="#b388ff")
        self.notes_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def save_note(self):
        note = self.notes_text.get("1.0", tk.END).strip()
        if not note:
            messagebox.showerror("Missing Note", "Please type a note before saving.")
            return

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (note, created_at) VALUES (?, ?)", (note, created_at))
        conn.commit()
        conn.close()
        
        self.notes_text.delete("1.0", tk.END)
        self.refresh_all()

    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT created_at, note FROM notes ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            preview = row[1][:75] + "..." if len(row[1]) > 75 else row[1]
            self.notes_listbox.insert(tk.END, f"{row[0]} - {preview}")
            
              # STUDY TIMER TAB
    # This is a simple Pomodoro-style timer to help students focus.
    
    def build_timer_tab(self):
        timer_card = tk.Frame(self.timer_frame, bg="white", padx=40, pady=40, highlightbackground="#ffd6e0", highlightthickness=2)
        timer_card.pack(expand=True)

        tk.Label(timer_card, text="Focus Timer 🌸", font=("Segoe UI", 24, "bold"), bg="white", fg="#4a3f55").pack(pady=10)

        self.timer_label = tk.Label(timer_card, text="25:00", font=("Segoe UI", 58, "bold"), bg="white", fg="#ff8fab")
        self.timer_label.pack(pady=20)

        button_frame = tk.Frame(timer_card, bg="white")
        button_frame.pack()

        ttk.Button(button_frame, text="Start", style="Cute.TButton", command=self.start_timer).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Pause", style="Cute.TButton", command=self.pause_timer).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Reset", style="Cute.TButton", command=self.reset_timer).grid(row=0, column=2, padx=10)
        
    def update_timer_label(self):
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.countdown()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 25 * 60
        self.update_timer_label()

    def countdown(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.update_timer_label()
            self.root.after(1000, self.countdown)
        elif self.timer_seconds == 0:
            self.timer_running = False
            messagebox.showinfo("Timer Done", "Great job! Take a short break.")
            self.reset_timer()
            
             # REFRESH AND STATUS METHODS
    # These update the tables, dashboard numbers, and bottom status bar.

    def refresh_all(self):
        self.load_assignments()
        self.load_tasks()
        self.load_notes()
        self.update_dashboard_counts()
        self.update_status_bar()

    def update_dashboard_counts(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM assignments")
        assignment_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM notes")
        note_count = cursor.fetchone()[0]

        conn.close()

        self.assignment_count_label.config(text=str(assignment_count))
        self.task_count_label.config(text=str(task_count))
        self.note_count_label.config(text=str(note_count))

    def update_status_bar(self):
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"  Today: {today}  |  Time: {current_time}  |  Database: {DB_NAME}")
        self.root.after(1000, self.update_status_bar)
        
        

        
        