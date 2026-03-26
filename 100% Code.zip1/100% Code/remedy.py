import subprocess
import sys
import tkinter as tk
from tkinter import ttk

from ui_theme import apply_theme


def launch(script_name: str) -> None:
    subprocess.call([sys.executable, script_name])


root = tk.Tk()
root.title("Remedy Guidance • Diabetes Tracker")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
apply_theme(root)

page = ttk.Frame(root, style="Root.TFrame", padding=24)
page.pack(fill="both", expand=True)

ttk.Label(page, text="Remedies & Next Steps", style="Title.TLabel").pack(anchor="w")
ttk.Label(page, text="Actionable and clinically aligned recommendations", style="Muted.TLabel").pack(anchor="w", pady=(4, 16))

card = ttk.Frame(page, style="Card.TFrame", padding=24)
card.pack(fill="x")

points = [
    "Clinical validation: discuss model output with a qualified healthcare professional.",
    "Interpretability: review why a prediction was made before taking action.",
    "Patient education: explain model strengths and limitations clearly.",
    "Lifestyle plan: monitor glucose trends, diet, activity, and medication adherence.",
]

ttk.Label(card, text="Care Guidance", style="Heading.TLabel").pack(anchor="w")
for p in points:
    ttk.Label(card, text=f"• {p}", style="Body.TLabel", wraplength=980, justify="left").pack(anchor="w", pady=(8, 0))

footer = ttk.Frame(page, style="Root.TFrame")
footer.pack(fill="x", side="bottom", pady=(16, 0))
ttk.Button(footer, text="Back to Dashboard", style="Secondary.TButton", command=lambda: [launch("master_GUI.py"), root.destroy()]).pack(side="left")
ttk.Button(footer, text="Home", style="Secondary.TButton", command=lambda: [launch("gui main.py"), root.destroy()]).pack(side="left", padx=(10, 0))
ttk.Button(footer, text="Exit", style="Danger.TButton", command=root.destroy).pack(side="right")

root.mainloop()
