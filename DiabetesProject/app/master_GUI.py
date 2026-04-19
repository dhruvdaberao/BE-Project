import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui_theme import apply_theme, fade_in


def launch(script_name: str) -> None:
    subprocess.call([sys.executable, script_name])


root = tk.Tk()
root.title("Dashboard • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)
fade_in(root)

page = ttk.Frame(root, style="Root.TFrame", padding=24)
page.pack(fill="both", expand=True)

header = ttk.Frame(page, style="Root.TFrame")
header.pack(fill="x", pady=(0, 16))

ttk.Label(header, text="Diabetes Tracker Dashboard", style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Minimal and focused workspace for screening, analysis, and guidance.", style="HeroBody.TLabel").pack(anchor="w", pady=(4, 0))

content = ttk.Frame(page, style="Root.TFrame")
content.pack(fill="both", expand=True)

sidebar = ttk.Frame(content, style="Nav.TFrame", padding=16)
sidebar.pack(side="left", fill="y", padx=(0, 16))

ttk.Label(sidebar, text="Navigation", style="Subheading.TLabel").pack(anchor="w", pady=(0, 10))
for item in ["Overview", "Prediction", "Analysis", "Remedy"]:
    ttk.Button(sidebar, text=item, style="Ghost.TButton").pack(fill="x", pady=4)

main = ttk.Frame(content, style="Root.TFrame")
main.pack(side="left", fill="both", expand=True)

stats = ttk.Frame(main, style="Root.TFrame")
stats.pack(fill="x", pady=(0, 14))
for idx, (title, desc) in enumerate([
    ("Risk Screening", "Model-powered diabetic risk check."),
    ("Analysis", "Clinical context and summary insights."),
    ("Recommendations", "Action-oriented next-step guidance."),
]):
    card = ttk.Frame(stats, style="SoftCard.TFrame", padding=16)
    card.grid(row=0, column=idx, sticky="nsew", padx=(0, 12 if idx < 2 else 0))
    ttk.Label(card, text=title, style="Subheading.TLabel").pack(anchor="w")
    ttk.Label(card, text=desc, style="Muted.TLabel", wraplength=260).pack(anchor="w", pady=(8, 0))
    stats.columnconfigure(idx, weight=1)

modules = ttk.Frame(main, style="Card.TFrame", padding=22)
modules.pack(fill="x")

ttk.Label(modules, text="Modules", style="Heading.TLabel").pack(anchor="w", pady=(0, 14))
btn_row = ttk.Frame(modules, style="Card.TFrame")
btn_row.pack(anchor="w")

ttk.Button(btn_row, text="Diabetic Mellitus", style="Primary.TButton", command=lambda: [launch("GUI_Master_old.py"), root.destroy()]).pack(side="left", padx=(0, 10))
ttk.Button(btn_row, text="Analysis", style="Secondary.TButton", command=lambda: [launch("analysis.py"), root.destroy()]).pack(side="left", padx=(0, 10))
ttk.Button(btn_row, text="Remedy", style="Secondary.TButton", command=lambda: [launch("remedy.py"), root.destroy()]).pack(side="left")

footer = ttk.Frame(page, style="Root.TFrame")
footer.pack(fill="x", side="bottom", pady=(16, 0))
ttk.Button(footer, text="Back", style="Ghost.TButton", command=lambda: [launch("gui main.py"), root.destroy()]).pack(side="left")
ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

root.mainloop()
