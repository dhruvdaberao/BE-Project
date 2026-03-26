import tkinter as tk
from tkinter import ttk

PALETTE = {
    "bg": "#f4f7fb",
    "surface": "#ffffff",
    "surface_alt": "#eef3f9",
    "text": "#0f172a",
    "muted": "#5b6b84",
    "primary": "#0f766e",
    "primary_hover": "#0d9488",
    "secondary": "#e2e8f0",
    "secondary_hover": "#cbd5e1",
    "success": "#0f9d58",
    "warning": "#d97706",
    "danger": "#dc2626",
    "border": "#dbe4ef",
}


def apply_theme(root: tk.Tk) -> ttk.Style:
    root.configure(bg=PALETTE["bg"])
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Root.TFrame", background=PALETTE["bg"])
    style.configure("Card.TFrame", background=PALETTE["surface"], relief="flat")
    style.configure("Header.TFrame", background=PALETTE["surface"])

    style.configure("Title.TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=("Segoe UI", 24, "bold"))
    style.configure("Heading.TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=("Segoe UI", 14, "bold"))
    style.configure("Body.TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=("Segoe UI", 11))
    style.configure("Muted.TLabel", background=PALETTE["surface"], foreground=PALETTE["muted"], font=("Segoe UI", 10))

    style.configure("TEntry", fieldbackground=PALETTE["surface_alt"], foreground=PALETTE["text"], bordercolor=PALETTE["border"], lightcolor=PALETTE["border"], darkcolor=PALETTE["border"], padding=8)
    style.map("TEntry", bordercolor=[("focus", PALETTE["primary"])], lightcolor=[("focus", PALETTE["primary"])], darkcolor=[("focus", PALETTE["primary"])])

    style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=(14, 10), foreground="#ffffff", background=PALETTE["primary"], borderwidth=0)
    style.map("Primary.TButton", background=[("active", PALETTE["primary_hover"])])

    style.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9), foreground=PALETTE["text"], background=PALETTE["secondary"], borderwidth=0)
    style.map("Secondary.TButton", background=[("active", PALETTE["secondary_hover"])])

    style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9), foreground="#ffffff", background=PALETTE["danger"], borderwidth=0)
    style.map("Danger.TButton", background=[("active", "#b91c1c")])

    return style
