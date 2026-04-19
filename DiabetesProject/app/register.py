import re
import sqlite3
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk

from ui_theme import apply_theme, fade_in

root = tk.Tk()
root.title("Register • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)
fade_in(root)

fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
email = tk.StringVar()
phoneno = tk.StringVar()
password = tk.StringVar()
confirm_password = tk.StringVar()

with sqlite3.connect("evaluation.db") as db:
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS registration"
        "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, password TEXT)"
    )


def password_check(passwd: str) -> bool:
    special_sym = ["$", "@", "#", "%"]
    return (
        6 <= len(passwd) <= 20
        and any(char.isdigit() for char in passwd)
        and any(char.isupper() for char in passwd)
        and any(char.islower() for char in passwd)
        and any(char in special_sym for char in passwd)
    )


def launch(script_name: str) -> None:
    subprocess.call([sys.executable, script_name])
    root.destroy()


def insert() -> None:
    fname = fullname.get().strip()
    addr = address.get().strip()
    un = username.get().strip()
    mail = email.get().strip()
    mobile = phoneno.get().strip()
    pwd = password.get()
    cnpwd = confirm_password.get()

    with sqlite3.connect("evaluation.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM registration WHERE username = ?", (un,))
        existing = c.fetchall()

    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    if fname.isdigit() or fname == "":
        ms.showinfo("Message", "Please enter valid full name")
    elif addr == "":
        ms.showinfo("Message", "Please enter address")
    elif mail == "" or not re.search(regex, mail):
        ms.showinfo("Message", "Please enter valid email")
    elif len(mobile) != 10 or not mobile.isdigit():
        ms.showinfo("Message", "Please enter 10 digit mobile number")
    elif existing:
        ms.showerror("Error!", "Username taken, try a different one.")
    elif pwd == "":
        ms.showinfo("Message", "Please enter a valid password")
    elif not password_check(pwd):
        ms.showinfo("Message", "Password must contain uppercase, lowercase, number and symbol")
    elif pwd != cnpwd:
        ms.showinfo("Message", "Password and Confirm Password must match")
    else:
        with sqlite3.connect("evaluation.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO registration(Fullname, address, username, Email, Phoneno, password) VALUES(?,?,?,?,?,?)",
                (fname, addr, un, mail, mobile, pwd),
            )
            conn.commit()
        ms.showinfo("Success!", "Account Created Successfully!")
        launch("login.py")


page = ttk.Frame(root, style="Root.TFrame", padding=24)
page.pack(fill="both", expand=True)

card = ttk.Frame(page, style="Card.TFrame", padding=30)
card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5)

ttk.Label(card, text="Create account", style="Heading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
ttk.Label(card, text="Join the platform to access diabetic risk dashboards.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 16))

fields = [
    ("Full Name", fullname),
    ("Address", address),
    ("E-mail", email),
    ("Phone Number", phoneno),
    ("User Name", username),
]

for i, (label, var) in enumerate(fields):
    row_index = i * 2 + 2
    ttk.Label(card, text=label, style="Body.TLabel").grid(row=row_index, column=0, sticky="w", pady=(0, 4))
    ttk.Entry(card, textvariable=var).grid(row=row_index + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

base_row = len(fields) * 2 + 2

ttk.Label(card, text="Password", style="Body.TLabel").grid(row=base_row, column=0, sticky="w", pady=(0, 4))
ttk.Entry(card, textvariable=password, show="*").grid(row=base_row + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

ttk.Label(card, text="Confirm Password", style="Body.TLabel").grid(row=base_row + 2, column=0, sticky="w", pady=(0, 4))
ttk.Entry(card, textvariable=confirm_password, show="*").grid(row=base_row + 3, column=0, columnspan=2, sticky="ew", pady=(0, 18))

actions = ttk.Frame(card, style="Card.TFrame")
actions.grid(row=base_row + 4, column=0, columnspan=2, sticky="w")
ttk.Button(actions, text="Register", style="Primary.TButton", command=insert).pack(side="left", padx=(0, 10))
ttk.Button(actions, text="Back to Login", style="Secondary.TButton", command=lambda: launch("login.py")).pack(side="left")

card.columnconfigure(0, weight=1)
card.columnconfigure(1, weight=1)

footer = ttk.Frame(page, style="Root.TFrame")
footer.pack(fill="x", side="bottom")
ttk.Button(footer, text="Home", style="Ghost.TButton", command=lambda: launch("gui main.py")).pack(side="left")
ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

root.mainloop()
