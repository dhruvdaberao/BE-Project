import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time


##############################################+=============================================================
root = tk.Tk()
root.configure(background="seashell2")
root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Home Page")




# #####For background Image
image2 = Image.open('12.webp')
image2 = image2.resize((w, h), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)





lbl = tk.Label(root, text="Diabetic Mellitus Detection System", font=('times', 30,' bold '), width=70,height=2,bg="#B0E0E6",fg="black")
lbl.place(x=0, y=0)



#################################################################################################################
def Main():
    from subprocess import call
    call(["python","GUI_Master_DFU.py"])
def Main1():
    from subprocess import call
    call(["python","GUI_Master_old.py"])
    
def reg():
    from subprocess import call
    call(["python","analysis.py"])
def log():
    from subprocess import call
    call(["python","remedy.py"])

def window():
    root.destroy()




# button5 = tk.Button(root, text="ULCER", command=Main,width=18, height=2, font=('times', 15, ' bold '),bg="black",fg="white")
# button5.place(x=1150, y=250)

button5 = tk.Button(root, text="DIABETIC MELLITUS", command=Main1,width=18, height=2, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
button5.place(x=1150, y=350)

button5 = tk.Button(root, text="ANALYSIS", command=reg,width=18, height=2, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
button5.place(x=1150, y=450)

button5 = tk.Button(root, text="REMEDY", command=log,width=18, height=2, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
button5.place(x=1150, y=550)




exit = tk.Button(root, text="Exit", command=window, width=18, height=2,bg="red", font=('times', 15, ' bold '),fg="white")
exit.place(x=1170, y=650)



root.mainloop()




# import tkinter as tk
# from tkinter import ttk
# import os, sys

# PALETTE = {'BG': '#0f172a', 'BG_DARK': '#0b1220', 'CARD': '#111827', 'CARD_ALT': '#0b1220', 'TEXT': '#e5e7eb', 'MUTED': '#9ca3af', 'PRIMARY': '#6366f1', 'PRIMARY_HL': '#818cf8', 'ACCENT': '#22d3ee', 'DANGER': '#ef4444', 'SUCCESS': '#10b981'}

# def apply_theme(root: tk.Tk):
#     root.configure(bg=PALETTE["BG"])
#     style = ttk.Style()
#     try:
#         style.theme_use("clam")
#     except:
#         pass
#     style.configure("Title.TLabel", background=PALETTE["BG"], foreground=PALETTE["TEXT"], font=("Segoe UI", 22, "bold"))
#     style.configure("Sub.TLabel", background=PALETTE["BG"], foreground=PALETTE["MUTED"], font=("Segoe UI", 11))
#     style.configure("Nav.TFrame", background=PALETTE["BG"])
#     style.configure("Card.TFrame", background=PALETTE["CARD"])
#     style.configure("Nav.TButton", padding=12)
#     style.map("Primary.TButton",
#               background=[("!disabled", PALETTE["PRIMARY"]), ("active", PALETTE["PRIMARY_HL"])],
#               foreground=[("!disabled", "white")])

# class HomeApp:
#     def __init__(self, root: tk.Tk):
#         self.root = root
#         self.root.title("Home • Diabetic Mellitus Detection")
#         self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#         apply_theme(self.root)

#         header = ttk.Frame(self.root, style="Nav.TFrame")
#         header.pack(fill="x", side="top")
#         ttk.Label(header, text="Diabetic Mellitus Detection System", style="Title.TLabel").pack(anchor="w", padx=24, pady=(16,0))
#         ttk.Label(header, text="Modern UI • Theme #5", style="Sub.TLabel").pack(anchor="w", padx=24, pady=(0,16))

#         main = ttk.Frame(self.root, style="Nav.TFrame")
#         main.pack(expand=True, fill="both")

#         grid = ttk.Frame(main, style="Nav.TFrame")
#         grid.pack()
#         cards = [
#             ("Diabetic Mellitus", lambda: self.launch("GUI_Master_old.py")),
#             ("Analysis",          lambda: self.launch("analysis.py")),
#             ("Remedy",            lambda: self.launch("remedy.py")),
#         ]

#         for i, (label, cmd) in enumerate(cards):
#             card = ttk.Frame(grid, style="Card.TFrame", padding=24)
#             card.grid(row=0, column=i, padx=12, pady=12, sticky="nsew")
#             ttk.Label(card, text=label, font=("Segoe UI", 16, "bold")).pack(anchor="w")
#             ttk.Label(card, text="Open module", style="Muted.TLabel").pack(anchor="w", pady=(0,12))
#             ttk.Button(card, text="Open", style="Primary.TButton", command=cmd).pack(anchor="w")

#         footer = ttk.Frame(self.root, style="Nav.TFrame")
#         footer.pack(side="bottom", fill="x")
#         ttk.Button(footer, text="Logout", command=lambda: self.launch("login.py")).pack(side="right", padx=16, pady=12)
#         ttk.Button(footer, text="Exit", command=self.root.destroy).pack(side="right", padx=8, pady=12)

#     def launch(self, filename):
#         os.system(f"{{sys.executable}} {filename}")
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = HomeApp(root)
#     root.mainloop()
