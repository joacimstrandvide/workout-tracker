# Importer
import tkinter as tk
from tkinter import ttk
import json
import datetime

# Data för veckor och antal sessioner per vecka
NUM_WEEKS = 52
SESSIONS_PER_WEEK = 3
SAVE_FILE = "training_progress.json"

# Läs in datan
def load_data():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    for week in range(1, NUM_WEEKS + 1):
        if str(week) not in data:
            data[str(week)] = [False] * SESSIONS_PER_WEEK
    return data

# Spara
def save_data():
    with open(SAVE_FILE, "w") as f:
        json.dump(progress_data, f)

# Skapa fönstret
root = tk.Tk()
root.title("Tränings Schema")
root.geometry("450x600")

progress_data = load_data()
checkbox_vars = {}
# Titel
header = ttk.Label(root, text="Tränings Schema",
                   font=("Segoe UI", 16, "bold"))
header.pack(pady=10)


canvas = tk.Canvas(root)
scroll_frame = ttk.Frame(canvas)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


scroll_frame.bind("<Configure>", on_configure)

# Skapa varje vecka
for week in range(1, NUM_WEEKS + 1):
    week_label = ttk.Label(
        scroll_frame, text=f"Vecka {week}", font=("Segoe UI", 12, "bold"))
    week_label.grid(row=week, column=0, padx=10, pady=5, sticky="w")

    checkbox_vars[week] = []
    for session in range(SESSIONS_PER_WEEK):
        var = tk.BooleanVar(value=progress_data[str(week)][session])
        cb = ttk.Checkbutton(
            scroll_frame, text=f"Pass {session + 1}", variable=var)
        cb.grid(row=week, column=session + 1, padx=5, pady=5)
        checkbox_vars[week].append(var)


def save_progress():
    for week in range(1, NUM_WEEKS + 1):
        progress_data[str(week)] = [v.get() for v in checkbox_vars[week]]
    save_data()
    ttk.Label(root, text="Sparat!", foreground="green").pack()

# Spara knappen
save_button = ttk.Button(root, text="Spara", command=save_progress)
save_button.pack(pady=15)

root.mainloop()
