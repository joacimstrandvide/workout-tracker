# Importer
import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk

# Antal veckor och antal pass per vecka
NUM_WEEKS = 52
SESSIONS_PER_WEEK = 3
SAVE_FILE = "training_progress.json"


class WorkoutTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Skapa Fönstret
        self.title("Tränings Schema")
        self.geometry("700x500")
        self.iconbitmap('assets/icon.ico')

        # Ladda datan
        self.progress_data = self.load_data()
        self.checkbox_vars = {}

        # Layouten
        self.create_notebook()
        self.create_week_tab()
        self.create_profile_tab()

        # Updatera förloppsindikatorn
        self.update_progress_bar()

    # Ladda datan
    def load_data(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        for week in range(1, NUM_WEEKS + 1):
            if str(week) not in data:
                data[str(week)] = [False] * SESSIONS_PER_WEEK
        return data

    def save_data(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.progress_data, f)

   # Notebooks funktion
    def create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.week_frame = ttk.Frame(self.notebook)
        self.profile_frame = ttk.Frame(self.notebook)

        self.week_frame.pack(fill="both", expand=True)
        self.profile_frame.pack(fill="both", expand=True)

        self.notebook.add(self.week_frame, text="Veckor")
        self.notebook.add(self.profile_frame, text="Profil")

    # Veckor tabben
    def create_week_tab(self):
        header = ttk.Label(
            self.week_frame, text="Tränings Schema", font=("Segoe UI", 16, "bold")
        )
        header.pack(pady=10)

        canvas = tk.Canvas(self.week_frame)
        scrollbar = ttk.Scrollbar(
            self.week_frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Skapa check boxes för varje vecka
        for week in range(1, NUM_WEEKS + 1):
            week_label = ttk.Label(
                scroll_frame, text=f"Vecka {week}", font=("Segoe UI", 12, "bold")
            )
            week_label.grid(row=week, column=0, padx=10, pady=5, sticky="w")

            self.checkbox_vars[week] = []
            for session in range(SESSIONS_PER_WEEK):
                var = tk.BooleanVar(
                    value=self.progress_data[str(week)][session])

                # Varje kryssruta uppdaterar förloppsindikatorn när den fylls i.
                cb = ttk.Checkbutton(
                    scroll_frame,
                    text=f"Pass {session + 1}",
                    variable=var,
                    command=self.update_progress_bar
                )
                cb.grid(row=week, column=session + 1, padx=5, pady=5)
                self.checkbox_vars[week].append(var)

        # Spara Knappen
        save_button = ttk.Button(
            self.week_frame, text="Spara", command=self.save_progress)
        save_button.pack(pady=15)

        self.save_label = ttk.Label(self.week_frame, text="")
        self.save_label.pack()

    # Profil
    def create_profile_tab(self):
        title = ttk.Label(
            self.profile_frame, text="Din Profil", font=("Segoe UI", 16, "bold")
        )
        title.pack(pady=20)

        self.progress_label = ttk.Label(
            self.profile_frame, text="Framsteg: 0%", font=("Segoe UI", 12))
        self.progress_label.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.profile_frame, variable=self.progress_var, maximum=100, length=400
        )
        self.progress_bar.pack(pady=10)

        note = ttk.Label(
            self.profile_frame,
            text="Fylls upp automatiskt när du markerar dina träningspass.",
            font=("Segoe UI", 10)
        )
        note.pack(pady=10)

        self.photo = tk.PhotoImage(file="assets/muscle.png")

        image_label = ttk.Label(
            self.profile_frame,
            image=self.photo,
            padding=10
        )
        image_label.pack(pady=10)

    def save_progress(self):
        for week in range(1, NUM_WEEKS + 1):
            self.progress_data[str(week)] = [v.get()
                                             for v in self.checkbox_vars[week]]
        self.save_data()
        self.update_progress_bar()
        self.save_label.config(text="Sparat!", foreground="green")

    def update_progress_bar(self):
        total_sessions = NUM_WEEKS * SESSIONS_PER_WEEK
        completed = 0

        for week in range(1, NUM_WEEKS + 1):
            completed += sum(v.get() for v in self.checkbox_vars[week])

        percent = round((completed / total_sessions) * 100, 1)
        self.progress_var.set(percent)
        self.progress_label.config(text=f"Framsteg: {percent}%")

        for week in range(1, NUM_WEEKS + 1):
            self.progress_data[str(week)] = [v.get()
                                             for v in self.checkbox_vars[week]]
        self.save_data()


if __name__ == "__main__":
    app = WorkoutTrackerApp()
    app.mainloop()
