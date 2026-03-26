import sqlite3
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk

from ui_theme import apply_theme


root = tk.Tk()
root.title("Login • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)

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
        cursor.execute(
            "SELECT * FROM registration WHERE username = ? AND password = ?",
            (username_val, password_val),
        )
        result = cursor.fetchall()

    if result:
        ms.showinfo("Success", "Login successful!")
        launch("GUI_Master_old.py")
    else:
        ms.showerror("Error", "Invalid username or password")


wrap = ttk.Frame(root, style="Root.TFrame", padding=24)
wrap.pack(fill="both", expand=True)

top = ttk.Frame(wrap, style="Root.TFrame")
top.pack(fill="x", pady=(0, 12))

ttk.Label(top, text="Diabetes Tracker", style="Title.TLabel").pack(anchor="w")
ttk.Label(top, text="Sign in to continue monitoring and analysis", style="Muted.TLabel").pack(anchor="w", pady=(4, 0))

card = ttk.Frame(wrap, style="Card.TFrame", padding=28)
card.pack(anchor="center", pady=40)


ttk.Label(card, text="Secure Login", style="Heading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))
ttk.Label(card, text="Username", style="Body.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 6))
user_entry = ttk.Entry(card, textvariable=username, width=36)
user_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

ttk.Label(card, text="Password", style="Body.TLabel").grid(row=3, column=0, sticky="w", pady=(0, 6))
pass_entry = ttk.Entry(card, textvariable=password, show="*", width=36)
pass_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 16))

btns = ttk.Frame(card, style="Card.TFrame")
btns.grid(row=5, column=0, columnspan=2, sticky="ew")

ttk.Button(btns, text="Login", style="Primary.TButton", command=login).pack(side="left", padx=(0, 10))
ttk.Button(btns, text="Create Account", style="Secondary.TButton", command=lambda: launch("register.py")).pack(side="left")

actions = ttk.Frame(wrap, style="Root.TFrame")
actions.pack(fill="x", side="bottom")

ttk.Button(actions, text="Home", style="Secondary.TButton", command=lambda: launch("gui main.py")).pack(side="left")
ttk.Button(actions, text="Register", style="Secondary.TButton", command=lambda: launch("register.py")).pack(side="left", padx=(10, 0))
ttk.Button(actions, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

user_entry.focus_set()
root.mainloop()
