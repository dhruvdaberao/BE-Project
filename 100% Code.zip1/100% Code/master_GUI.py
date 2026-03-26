import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui_theme import apply_theme


def launch(script_name: str) -> None:
    subprocess.call([sys.executable, script_name])


root = tk.Tk()
root.title("Dashboard • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)

page = ttk.Frame(root, style="Root.TFrame", padding=24)
page.pack(fill="both", expand=True)

ttk.Label(page, text="Diabetes Tracker Dashboard", style="Title.TLabel").pack(anchor="w")
ttk.Label(page, text="Choose a module to continue", style="Muted.TLabel").pack(anchor="w", pady=(4, 18))

stats = ttk.Frame(page, style="Root.TFrame")
stats.pack(fill="x", pady=(0, 16))

for item in [
    ("Risk Screening", "Model-based diabetic risk check"),
    ("Analysis", "Interpret spread and disease context"),
    ("Remedy", "Review best-practice guidance"),
]:
    card = ttk.Frame(stats, style="Card.TFrame", padding=16)
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    ttk.Label(card, text=item[0], style="Heading.TLabel").pack(anchor="w")
    ttk.Label(card, text=item[1], style="Muted.TLabel", wraplength=260).pack(anchor="w", pady=(6, 0))

modules = ttk.Frame(page, style="Card.TFrame", padding=24)
modules.pack(fill="x")

ttk.Label(modules, text="Modules", style="Heading.TLabel").pack(anchor="w", pady=(0, 12))

btn_row = ttk.Frame(modules, style="Card.TFrame")
btn_row.pack(anchor="w")

ttk.Button(btn_row, text="Diabetic Mellitus", style="Primary.TButton", command=lambda: [launch("GUI_Master_old.py"), root.destroy()]).pack(side="left", padx=(0, 10))
ttk.Button(btn_row, text="Analysis", style="Secondary.TButton", command=lambda: [launch("analysis.py"), root.destroy()]).pack(side="left", padx=(0, 10))
ttk.Button(btn_row, text="Remedy", style="Secondary.TButton", command=lambda: [launch("remedy.py"), root.destroy()]).pack(side="left")

footer = ttk.Frame(page, style="Root.TFrame")
footer.pack(fill="x", side="bottom", pady=(16, 0))

ttk.Button(footer, text="Back", style="Secondary.TButton", command=lambda: [launch("gui main.py"), root.destroy()]).pack(side="left")
ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

root.mainloop()
