import tkinter as tk
from tkinter import ttk

PALETTE = {
    "bg": "#f4f8ff",
    "bg_alt": "#edf3ff",
    "surface": "#fbfdff",
    "surface_alt": "#f2f7ff",
    "text": "#0f1f3d",
    "muted": "#5f7094",
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "primary_soft": "#dbeafe",
    "secondary": "#ffffff",
    "secondary_hover": "#f0f6ff",
    "danger": "#dc2626",
    "danger_hover": "#b91c1c",
    "border": "#d8e4f8",
    "focus": "#93c5fd",
}

FONT_FAMILY = "Poppins"


def font(size: int, weight: str = "normal") -> tuple[str, int, str]:
    return (FONT_FAMILY, size, weight)


def fade_in(window: tk.Tk | tk.Toplevel, step: float = 0.08, delay: int = 18) -> None:
    window.attributes("-alpha", 0.0)

    def _next(alpha: float) -> None:
        alpha = min(alpha + step, 1.0)
        window.attributes("-alpha", alpha)
        if alpha < 1.0:
            window.after(delay, lambda: _next(alpha))

    window.after(delay, lambda: _next(0.0))


def apply_theme(root: tk.Tk) -> ttk.Style:
    root.configure(bg=PALETTE["bg"])
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Root.TFrame", background=PALETTE["bg"])
    style.configure("Header.TFrame", background=PALETTE["bg"])
    style.configure("Card.TFrame", background=PALETTE["surface"], borderwidth=1, relief="solid")
    style.configure("SoftCard.TFrame", background=PALETTE["surface_alt"], borderwidth=1, relief="solid")
    style.configure("Nav.TFrame", background=PALETTE["surface"], borderwidth=1, relief="solid")

    style.configure("Title.TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=font(26, "bold"))
    style.configure("Heading.TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=font(15, "bold"))
    style.configure("Subheading.TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=font(12, "bold"))
    style.configure("Body.TLabel", background=PALETTE["surface"], foreground=PALETTE["text"], font=font(11, "normal"))
    style.configure("Muted.TLabel", background=PALETTE["surface"], foreground=PALETTE["muted"], font=font(10, "normal"))
    style.configure("HeroBody.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=font(11, "normal"))

    style.configure(
        "TEntry",
        fieldbackground=PALETTE["secondary"],
        foreground=PALETTE["text"],
        bordercolor=PALETTE["border"],
        lightcolor=PALETTE["border"],
        darkcolor=PALETTE["border"],
        insertcolor=PALETTE["primary"],
        padding=(12, 10),
        font=font(11),
    )
    style.map(
        "TEntry",
        bordercolor=[("focus", PALETTE["primary"])],
        lightcolor=[("focus", PALETTE["focus"])],
        darkcolor=[("focus", PALETTE["focus"])],
    )

    style.configure(
        "Primary.TButton",
        font=font(11, "bold"),
        padding=(16, 10),
        foreground="#ffffff",
        background=PALETTE["primary"],
        bordercolor=PALETTE["primary"],
        relief="flat",
    )
    style.map("Primary.TButton", background=[("active", PALETTE["primary_hover"])])

    style.configure(
        "Secondary.TButton",
        font=font(11, "bold"),
        padding=(16, 10),
        foreground=PALETTE["primary"],
        background=PALETTE["secondary"],
        bordercolor=PALETTE["border"],
        relief="flat",
    )
    style.map("Secondary.TButton", background=[("active", PALETTE["secondary_hover"])])

    style.configure(
        "Ghost.TButton",
        font=font(10, "bold"),
        padding=(14, 9),
        foreground=PALETTE["muted"],
        background=PALETTE["surface"],
        bordercolor=PALETTE["surface"],
        relief="flat",
    )
    style.map("Ghost.TButton", background=[("active", PALETTE["primary_soft"])], foreground=[("active", PALETTE["primary"])])

    style.configure(
        "Danger.TButton",
        font=font(11, "bold"),
        padding=(16, 10),
        foreground="#ffffff",
        background=PALETTE["danger"],
        bordercolor=PALETTE["danger"],
        relief="flat",
    )
    style.map("Danger.TButton", background=[("active", PALETTE["danger_hover"])])

    return style
