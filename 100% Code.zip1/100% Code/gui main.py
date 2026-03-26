import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui_theme import apply_theme


def launch(script_name: str, root: tk.Tk) -> None:
    subprocess.call([sys.executable, script_name])
    root.destroy()


root = tk.Tk()
root.title("Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)

container = ttk.Frame(root, style="Root.TFrame", padding=24)
container.pack(fill="both", expand=True)

header = ttk.Frame(container, style="Root.TFrame")
header.pack(fill="x", pady=(0, 18))

hero = ttk.Frame(container, style="Card.TFrame", padding=28)
hero.pack(fill="x", pady=(0, 16))

footer = ttk.Frame(container, style="Root.TFrame")
footer.pack(fill="x", side="bottom", pady=(16, 0))


ttk.Label(header, text="Diabetes Tracker", style="Title.TLabel").pack(anchor="w")
ttk.Label(
    header,
    text="Early diabetic risk support using foot thermography insights",
    style="Muted.TLabel",
).pack(anchor="w", pady=(4, 0))

ttk.Label(hero, text="Welcome", style="Heading.TLabel").pack(anchor="w")
ttk.Label(
    hero,
    text=(
        "Securely access screening workflows, maintain patient entries, and "
        "review guidance in a clean healthcare-focused interface."
    ),
    style="Body.TLabel",
    wraplength=860,
    justify="left",
).pack(anchor="w", pady=(8, 18))

actions = ttk.Frame(hero, style="Card.TFrame")
actions.pack(anchor="w")

ttk.Button(actions, text="Sign In", style="Primary.TButton", command=lambda: launch("login.py", root)).pack(side="left", padx=(0, 10))
ttk.Button(actions, text="Create Account", style="Secondary.TButton", command=lambda: launch("register.py", root)).pack(side="left")

ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

root.mainloop()
