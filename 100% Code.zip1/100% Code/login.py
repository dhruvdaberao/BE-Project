import tkinter as tk
from tkinter import ttk, LEFT, END
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
#import re


##############################################+=============================================================
root = tk.Tk()
root.configure(background="white")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("LOGIN")




username = tk.StringVar()
password = tk.StringVar()
        

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('4.jpg')
image2 = image2.resize((w,h), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)



#
label_l1 = tk.Label(root, text="Dibetes Mellitus Using Foot Thermography",font=("Times New Roman", 30, 'bold'),
                    background="skyblue", fg="white", width=67, height=2)
label_l1.place(x=0, y=0)

img = Image.open('7.png')
img = img.resize((100,70), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(img)

logo_label = tk.Label(root, image=logo_image)
logo_label.image = logo_image
logo_label.place(x=40, y=10)


def registration():
    from subprocess import call
    call(["python","master_GUI.py"])
    root.destroy()

def login():
    username_val = username.get()
    password_val = password.get()

    # Connect to database
    db = sqlite3.connect('evaluation.db')
    cursor = db.cursor()

    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration
        (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)
    """)
    db.commit()

    # Check login credentials
    cursor.execute("SELECT * FROM registration WHERE username = ? AND password = ?", 
                   (username_val, password_val))
    result = cursor.fetchall()

    if result:
        ms.showinfo("Success", "Login successful!")
        root.destroy()
        from subprocess import call
        call(["python", "GUI_Master_old.py"])
    else:
        ms.showerror("Error", "Invalid username or password")



# frame_alpr = tk.LabelFrame(root, text=" --About us-- ", width=550, height=500, bd=5, font=('times', 14, ' bold '),bg="#7CCD7C")
# frame_alpr.grid(row=0, column=0, sticky='nw')
# frame_alpr.place(x=550, y=200)

# label_l2 = tk.Label(root, text="___ Login Form ___",font=("Times New Roman", 30, 'bold'),
#                     background="#EEEE00", fg="black", width=67, height=3)
# label_l2.place(x=0, y=90)


# bg1_icon=ImageTk.PhotoImage(file="m.jpg")

bg_icon=ImageTk.PhotoImage(file="L.jpg")
user_icon=ImageTk.PhotoImage(file="l1.png")
pass_icon=ImageTk.PhotoImage(file="p1.jpg")
        
# bg_lbl=tk.Label(root,image=bg1_icon, width=800,height=600)
# bg_lbl.place(x=430,y=130)
        
title=tk.Label(root, text="__Login Here__", font=("Times new roman", 30, "bold","italic"),bd=5,bg="white",fg="black")
title.place(x=700,y=150,width=250)
        
Login_frame=tk.Frame(root,bg="white")
Login_frame.place(x=550,y=250)
        
logolbl=tk.Label(Login_frame,image=bg_icon,bd=0).grid(row=0,columnspan=2,pady=20)
        
lbluser=tk.Label(Login_frame,text="Username",image=user_icon,compound=LEFT,font=("Times new roman", 20, "bold"),bg="white").grid(row=1,column=0,padx=20,pady=10)
txtuser=tk.Entry(Login_frame,bd=5,textvariable=username,font=("",15))
txtuser.grid(row=1,column=1,padx=20)
        
lblpass=tk.Label(Login_frame,text="Password",image=pass_icon,compound=LEFT,font=("Times new roman", 20, "bold"),bg="white").grid(row=2,column=0,padx=50,pady=10)
txtpass=tk.Entry(Login_frame,bd=5,textvariable=password,show="*",font=("",15))
txtpass.grid(row=2,column=1,padx=20)
        
btn_log=tk.Button(Login_frame,text="Login",command=login,width=15,font=("Times new roman", 14, "bold"),bg="Green",fg="black")
btn_log.grid(row=3,column=1,pady=10)
btn_reg=tk.Button(Login_frame,text="Create Account",command=registration,width=15,font=("Times new roman", 14, "bold"),bg="red",fg="black")
btn_reg.grid(row=3,column=0,pady=10)
        
        
    
       
        # Login Function



def log():
    from subprocess import call
    call(["python","gui main.py"])
    root.destroy()
    
def window():
  root.destroy()
  
  
def con():
    from subprocess import call
    call(["python","register.py"])
    root.destroy()

 #def about():
  #   from subprocess import call
   #  call(["python","aboutus.py"])
    # root.destroy()
    
    
button1 = tk.Button(label_l1, text="HOME", command=log, width=10, height=1,font=('times 15 bold '),bd=0, bg="skyblue", fg="white")
button1.place(x=1170, y=50)

button2 = tk.Button(label_l1, text="REGISTER",command=con,width=13, height=1,font=('times 15 bold '), bd=0,bg="skyblue", fg="white")
button2.place(x=1290, y=50)

button4 = tk.Button(label_l1, text="EXIT", command=window, width=10, height=1,font=('times 15 bold '),bd=0,bg="skyblue", fg="white")
button4.place(x=1430, y=50)




root.mainloop()




# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk
# import sqlite3
# import os
# import sys

# # ===== Theme #5 (Indigo/Cyan on Slate) =====
# PALETTE = {'BG': '#0f172a', 'BG_DARK': '#0b1220', 'CARD': '#111827', 'CARD_ALT': '#0b1220', 'TEXT': '#e5e7eb', 'MUTED': '#9ca3af', 'PRIMARY': '#6366f1', 'PRIMARY_HL': '#818cf8', 'ACCENT': '#22d3ee', 'DANGER': '#ef4444', 'SUCCESS': '#10b981'}

# def apply_theme(root: tk.Tk):
#     root.configure(bg=PALETTE["BG"])
#     style = ttk.Style()
#     try:
#         style.theme_use("clam")
#     except:
#         pass

#     style.configure("TLabel", background=PALETTE["CARD"], foreground=PALETTE["TEXT"])
#     style.configure("Muted.TLabel", background=PALETTE["CARD"], foreground=PALETTE["MUTED"])
#     style.configure("Title.TLabel", background=PALETTE["BG"], foreground=PALETTE["TEXT"], font=("Segoe UI", 22, "bold"))
#     style.configure("TEntry", fieldbackground=PALETTE["CARD_ALT"], foreground=PALETTE["TEXT"])
#     style.map("TEntry", fieldbackground=[("active", PALETTE["CARD_ALT"])], bordercolor=[("focus", PALETTE["PRIMARY"])])
#     style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"))
#     style.configure("TButton", padding=10)
#     style.map("Primary.TButton",
#               background=[("!disabled", PALETTE["PRIMARY"]), ("active", PALETTE["PRIMARY_HL"])],
#               foreground=[("!disabled", "white")])
#     style.map("TButton",
#               background=[("active", PALETTE["CARD_ALT"])],
#               foreground=[("!disabled", PALETTE["TEXT"])])

#     style.configure("Card.TFrame", background=PALETTE["CARD"], borderwidth=0)
#     style.configure("Nav.TFrame", background=PALETTE["BG"])

# class LoginApp:
#     def __init__(self, root: tk.Tk):
#         self.root = root
#         self.root.title("Login • Diabetic Mellitus Detection")
#         self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#         apply_theme(self.root)

#         self._accent = tk.Canvas(self.root, bg=PALETTE["BG"], highlightthickness=0, bd=0)
#         self._accent.place(relx=0, rely=0, relwidth=1, relheight=1)
#         try:
#             self._accent.create_oval(-200, -150, 500, 450, fill=PALETTE["PRIMARY"], outline="", stipple="gray25")
#             self._accent.create_oval(1000, 400, 1600, 1000, fill=PALETTE["ACCENT"], outline="", stipple="gray25")
#         except:
#             pass

#         header = ttk.Frame(self.root, style="Nav.TFrame")
#         header.pack(fill="x", side="top")
#         title = ttk.Label(header, text="Diabetic Mellitus Using Foot Thermography", style="Title.TLabel")
#         title.pack(padx=24, pady=16, side="left")

#         self.card = ttk.Frame(self.root, style="Card.TFrame")
#         self.card.place(relx=0.5, rely=0.5, anchor="center")
#         inner = ttk.Frame(self.card, style="Card.TFrame", padding=28)
#         inner.pack()

#         heading = ttk.Label(inner, text="Welcome back", font=("Segoe UI", 18, "bold"))
#         sub = ttk.Label(inner, text="Sign in to continue", style="Muted.TLabel")
#         heading.grid(row=0, column=0, columnspan=2, sticky="w")
#         sub.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 16))

#         ttk.Label(inner, text="Username").grid(row=2, column=0, sticky="w", pady=(6, 6))
#         self.username = ttk.Entry(inner, width=28)
#         self.username.grid(row=2, column=1, sticky="ew", pady=(6, 6))

#         ttk.Label(inner, text="Password").grid(row=3, column=0, sticky="w", pady=(6, 6))
#         self.password = ttk.Entry(inner, show="•", width=28)
#         self.password.grid(row=3, column=1, sticky="ew", pady=(6, 6))

#         btns = ttk.Frame(inner, style="Card.TFrame")
#         btns.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
#         login_btn = ttk.Button(btns, text="Login", style="Primary.TButton", command=self.login)
#         reg_btn = ttk.Button(btns, text="Create Account", command=self.go_register)
#         login_btn.pack(side="left", padx=(0, 8))
#         reg_btn.pack(side="left")

#         inner.columnconfigure(1, weight=1)

#         footer = ttk.Label(self.root, text="© 2025 DMFS • Modern UI v5", style="Muted.TLabel")
#         footer.pack(side="bottom", pady=12)

#     def _ensure_table(self, cursor):
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS registration
#             (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)
#         """)

#     def login(self):
#         u = self.username.get().strip()
#         p = self.password.get().strip()
#         if not u or not p:
#             messagebox.showerror("Invalid", "Please enter both username and password.")
#             return

#         db = sqlite3.connect('evaluation.db')
#         cur = db.cursor()
#         self._ensure_table(cur)
#         db.commit()

#         cur.execute("SELECT 1 FROM registration WHERE username = ? AND password = ?", (u, p))
#         row = cur.fetchone()
#         db.close()

#         if row:
#             messagebox.showinfo("Success", "Login successful!")
#             self.launch_script("master_GUI.py")
#             self.root.destroy()
#         else:
#             messagebox.showerror("Error", "Invalid username or password.")

#     def go_register(self):
#         self.launch_script("register.py")
#         self.root.destroy()

#     def launch_script(self, filename):
#         os.system(f"{{sys.executable}} {filename}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LoginApp(root)
#     root.mainloop()
