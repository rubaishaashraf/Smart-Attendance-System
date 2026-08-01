# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import csv
from datetime import datetime
import sys

# Get path to exe or folder
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to Attendance.py
ATTENDANCE_SCRIPT = os.path.join(BASE_DIR, "Attendance.py")

# Path to face data
DATA_FOLDER = os.path.join(BASE_DIR, "data")


ATTENDANCE_SCRIPT = os.path.join(BASE_DIR, "Attendance.py")
DATA_FOLDER = os.path.join(BASE_DIR, "data")


# GUI SETUP

root = tk.Tk()
root.title("Face Recognition Attendance")
root.geometry("700x400")
root.resizable(False, False)

title_label = tk.Label(root, text="Face Recognition Attendance System",
                       font=("Arial", 16))
title_label.pack(pady=10)

frame_main = tk.Frame(root)
frame_main.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
frame_buttons = tk.Frame(frame_main)
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=10)
frame_table = tk.Frame(frame_main)
frame_table.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

tree = ttk.Treeview(frame_table)
tree.pack(expand=True, fill=tk.BOTH)

tree['columns'] = ('Name', 'Time')
tree.heading("#0", text="")
tree.column("#0", width=0, stretch=tk.NO)
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, width=150)

def update_table():
    """
    Reads today's CSV and updates the GUI table.
    Called every 2 seconds.
    """
    ts = datetime.now()
    date_str = ts.strftime('%d-%m-%Y')
    csv_file = f"Attendance/Attendance_{date_str}.csv"

    # Clear old rows
    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        if len(rows) > 1:
            for row in rows[1:]:
                tree.insert("", tk.END, values=row)

    root.after(2000, update_table)  # refresh every 2 seconds

def mark_attendance():
    """
    Runs Attendance.py. The webcam will open and instructions appear on the screen.
    """
    if not os.path.exists(ATTENDANCE_SCRIPT):
        messagebox.showerror("Error", f"{ATTENDANCE_SCRIPT} not found!")
        return

    messagebox.showinfo("Instructions",
                        "The webcam will open.\n\n"
                        "- Press 'O' to mark attendance\n"
                        "- Press 'ESC' to exit\n"
                        "- Make sure your face is clearly visible to the camera.")

    # Run Attendance.py (user interacts with webcam)
    subprocess.run(["python", ATTENDANCE_SCRIPT])

attendance_btn = tk.Button(frame_buttons, text="Mark Attendance",
                           font=("Arial", 12), width=20, command=mark_attendance)
attendance_btn.pack(pady=10)

exit_btn = tk.Button(frame_buttons, text="Exit",
                     font=("Arial", 12), width=20, command=root.destroy)
exit_btn.pack(pady=10)

update_table()

# Run the GUI
root.mainloop()
