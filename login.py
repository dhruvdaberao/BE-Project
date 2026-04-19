import sqlite3
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk

from ui_theme import apply_theme, fade_in


root = tk.Tk()
root.title("Login • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)
fade_in(root)

username = tk.StringVar()
password = tk.StringVar()


def launch(script_name: str) -> None:
    subprocess.call([sys.executable, script_name])
    root.destroy()


def login() -> None:
    username_val = username.get().strip()
    password_val = password.get()

    with sqlite3.connect("evaluation.db") as db:
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registration
            (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)
            """
        )
        cursor.execute("SELECT * FROM registration WHERE username = ? AND password = ?", (username_val, password_val))
        result = cursor.fetchall()

    if result:
        ms.showinfo("Success", "Login successful!")
        launch("master_GUI.py")
    else:
        ms.showerror("Error", "Invalid username or password")


wrap = ttk.Frame(root, style="Root.TFrame", padding=24)
wrap.pack(fill="both", expand=True)

card = ttk.Frame(wrap, style="Card.TFrame", padding=32)
card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.42)

ttk.Label(card, text="Welcome back", style="Heading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
ttk.Label(card, text="Sign in to continue to your dashboard.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 20))

ttk.Label(card, text="Username", style="Body.TLabel").grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 6))
user_entry = ttk.Entry(card, textvariable=username)
user_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))

ttk.Label(card, text="Password", style="Body.TLabel").grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 6))
pass_entry = ttk.Entry(card, textvariable=password, show="*")
pass_entry.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 18))

card.columnconfigure(0, weight=1)
actions = ttk.Frame(card, style="Card.TFrame")
actions.grid(row=6, column=0, columnspan=2, sticky="ew")

ttk.Button(actions, text="Login", style="Primary.TButton", command=login).pack(side="left", padx=(0, 10))
ttk.Button(actions, text="Create Account", style="Secondary.TButton", command=lambda: launch("register.py")).pack(side="left")

footer = ttk.Frame(wrap, style="Root.TFrame")
footer.pack(fill="x", side="bottom")
ttk.Button(footer, text="Home", style="Ghost.TButton", command=lambda: launch("gui main.py")).pack(side="left")
ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

user_entry.focus_set()
root.mainloop()
