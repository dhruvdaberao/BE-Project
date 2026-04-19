import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui_theme import PALETTE, apply_theme, fade_in


def launch(script_name: str, root: tk.Tk) -> None:
    subprocess.call([sys.executable, script_name])
    root.destroy()


root = tk.Tk()
root.title("Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)
fade_in(root)

shell = ttk.Frame(root, style="Root.TFrame", padding=30)
shell.pack(fill="both", expand=True)

hero = ttk.Frame(shell, style="Card.TFrame", padding=34)
hero.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.68)

accent = tk.Frame(hero, bg=PALETTE["primary"], height=5)
accent.pack(fill="x", pady=(0, 18))

ttk.Label(hero, text="Diabetes Tracker", style="Title.TLabel").pack(anchor="w")
ttk.Label(
    hero,
    text="A clean and secure workflow for diabetic risk screening and patient support.",
    style="HeroBody.TLabel",
    wraplength=860,
    justify="left",
).pack(anchor="w", pady=(8, 24))

bullets = ttk.Frame(hero, style="Card.TFrame")
bullets.pack(fill="x", pady=(0, 24))
for text in [
    "• Fast image analysis and CNN prediction",
    "• Structured dashboard with simple navigation",
    "• Accessible, minimal interface for daily use",
]:
    ttk.Label(bullets, text=text, style="Body.TLabel").pack(anchor="w", pady=3)

actions = ttk.Frame(hero, style="Card.TFrame")
actions.pack(anchor="w")

ttk.Button(actions, text="Sign In", style="Primary.TButton", command=lambda: launch("login.py", root)).pack(side="left", padx=(0, 10))
ttk.Button(actions, text="Create Account", style="Secondary.TButton", command=lambda: launch("register.py", root)).pack(side="left")
ttk.Button(shell, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="bottom", anchor="e", pady=(16, 0))

root.mainloop()
