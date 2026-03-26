import tkinter as tk
#from tkinter import ttk, LEFT, END
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re

##############################################+=============================================================
root = tk.Tk()
root.configure(background="white")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("REGISTER")

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('6.webp')
image2 = image2.resize((w,h), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=500, y=0)  # , relwidth=1, relheight=1)




label_l1 = tk.Label(root, text=" Dibetes Mellitus Using Foot Thermography",font=("Times New Roman", 30, 'bold'),
                    background="skyblue", fg="white", width=67, height=2)
label_l1.place(x=0, y=0)

img = Image.open('7.png')
img = img.resize((100,70), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(img)

logo_label = tk.Label(root, image=logo_image)
logo_label.image = logo_image
logo_label.place(x=40, y=10)

# frame_alpr = tk.LabelFrame(root, text=" --About us-- ", width=550, height=500, bd=5, font=('times', 14, ' bold '),bg="#7CCD7C")
# frame_alpr.grid(row=0, column=0, sticky='nw')
# frame_alpr.place(x=550, y=200)

# label_l2 = tk.Label(root, text="___ Registration Form ___",font=("Times New Roman", 30, 'bold'),
#                     background="black", fg="white", width=67, height=2)
# label_l2.place(x=0, y=90)


frame_alpr = tk.LabelFrame(root, text=" --Register-- ", width=600, height=697, bd=5, font=('times', 14, ' bold '),fg="white",bg="gray")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=0, y=96)

######################### Registration form #####################################################################

Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Email = tk.StringVar()
Phoneno = tk.IntVar()
# var = tk.IntVar()
# age = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()



# database code
db = sqlite3.connect('evaluation.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS registration"
               "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, password TEXT)")
db.commit()



def password_check(passwd): 
	
	SpecialSym =['$', '@', '#', '%'] 
	val = True
	
	if len(passwd) < 6: 
		print('length should be at least 6') 
		val = False
		
	if len(passwd) > 20: 
		print('length should be not be greater than 8') 
		val = False
		
	if not any(char.isdigit() for char in passwd): 
		print('Password should have at least one numeral') 
		val = False
		
	if not any(char.isupper() for char in passwd): 
		print('Password should have at least one uppercase letter') 
		val = False
		
	if not any(char.islower() for char in passwd): 
		print('Password should have at least one lowercase letter') 
		val = False
		
	if not any(char in SpecialSym for char in passwd): 
		print('Password should have at least one of the symbols $@#') 
		val = False
	if val: 
		return val 

def insert():
    fname = Fullname.get()
    addr = address.get()
    un = username.get()
    email = Email.get()
    mobile = Phoneno.get()
    # gender = var.get()
    # time = age.get()
    pwd = password.get()
    cnpwd = password1.get()

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()

    # Find Existing username if any take proper action
    find_user = ('SELECT * FROM registration WHERE username = ?')
    c.execute(find_user, [(username.get())])

    # else:
    #   ms.showinfo('Success!', 'Account Created Successfully !')

    # to check mail
    #regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        a = True
    else:
        a = False
    # validation
    if (fname.isdigit() or (fname == "")):
        ms.showinfo("Message", "please enter valid name")
    elif (addr == ""):
        ms.showinfo("Message", "Please Enter Address")
    elif (email == "") or (a == False):
        ms.showinfo("Message", "Please Enter valid email")
    elif((len(str(mobile)))<10 or len(str((mobile)))>10):
        ms.showinfo("Message", "Please Enter 10 digit mobile number")
    # elif ((time > 100) or (time == 0)):
    #     ms.showinfo("Message", "Please Enter valid age")
    elif (c.fetchall()):
        ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
    elif (pwd == ""):
        ms.showinfo("Message", "Please Enter valid password")
    # elif (var == False):
    #     ms.showinfo("Message", "Please Enter gender")
    elif(pwd=="")or(password_check(pwd))!=True:
        ms.showinfo("Message", "password must contain atleast 1 Uppercase letter,1 symbol,1 number")
    elif (pwd != cnpwd):
        ms.showinfo("Message", "Password Confirm password must be same")
    else:
        conn = sqlite3.connect('evaluation.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO registration(Fullname, address, username, Email, Phoneno, password) VALUES(?,?,?,?,?,?)',
                (fname, addr, un, email, mobile, pwd))

            conn.commit()
            db.close()
            ms.showinfo('Success!', 'Account Created Successfully !')
            # window.destroy()
            root.destroy()
            from subprocess import call
            call(["python", "login.py"])
            

#####################################################################################################################################################



l1 = tk.Label(frame_alpr, text="Registration Form", font=("Times new roman", 30, "bold","italic"),bd=5, bg="gray", fg="white")
l1.place(x=120, y=10)

# that is for label1 registration

l2 = tk.Label(frame_alpr, text="Full Name :", width=12, font=("Times new roman", 15, "bold"),bd=5, fg="black")
l2.place(x=100, y=100)
t1 = tk.Entry(frame_alpr, textvar=Fullname, width=20, font=('', 15))
t1.place(x=300, y=100)
# that is for label 2 (full name)


l3 = tk.Label(frame_alpr, text="Address :", width=12, font=("Times new roman", 15, "bold"),bd=5, fg="black")
l3.place(x=100, y=150)
t2 = tk.Entry(frame_alpr, textvar=address, width=20, font=('', 15))
t2.place(x=300, y=150)
# that is for label 3(address)



# that is for label 4(blood group)

l5 = tk.Label(frame_alpr, text="E-mail :", width=12, font=("Times new roman", 15, "bold"), bd=5,fg="black")
l5.place(x=100, y=200)
t4 = tk.Entry(frame_alpr, textvar=Email, width=20, font=('', 15))
t4.place(x=300, y=200)
# that is for email address

l6 = tk.Label(frame_alpr, text="Phone number :", width=12, font=("Times new roman", 15, "bold"),bd=5, fg="black")
l6.place(x=100, y=250)
t5 = tk.Entry(frame_alpr, textvar=Phoneno, width=20, font=('', 15))
t5.place(x=300, y=250)
# phone number
# l7 = tk.Label(frame_alpr, text="Gender :", width=12, font=("Times new roman", 15, "bold"), bg="snow")
# l7.place(x=10, y=250)
# # gender
# tk.Radiobutton(frame_alpr, text="Male", padx=5, width=5, bg="snow", font=("bold", 15), variable=var, value=1).place(x=80,
#                                                                                                                 y=250)
# tk.Radiobutton(frame_alpr, text="Female", padx=20, width=4, bg="snow", font=("bold", 15), variable=var, value=2).place(
#     x=120, y=250)

# l8 = tk.Label(frame_alpr, text="Age :", width=12, font=("Times new roman", 15, "bold"), bg="snow")
# l8.place(x=10, y=400)
# t6 = tk.Entry(frame_alpr, textvar=age, width=20, font=('', 15))
# t6.place(x=80, y=400)

l4 = tk.Label(frame_alpr, text="User Name :", width=12, font=("Times new roman", 15, "bold"), bd=5,fg="black")
l4.place(x=100, y=300)
t3 = tk.Entry(frame_alpr, textvar=username, width=20, font=('', 15))
t3.place(x=300, y=300)

l9 = tk.Label(frame_alpr, text="Password :", width=12, font=("Times new roman", 15, "bold"),bd=5, fg="black")
l9.place(x=100, y=350)
t9 = tk.Entry(frame_alpr, textvar=password, width=20, font=('', 15), show="*")
t9.place(x=300, y=350)

l10 = tk.Label(frame_alpr, text="Confirm Password:", width=13, font=("Times new roman", 15, "bold"),bd=5, fg="black")
l10.place(x=100, y=400)

t10 = tk.Entry(frame_alpr, textvar=password1, width=20, font=('', 15), show="*")
t10.place(x=300, y=400)

btn = tk.Button(frame_alpr, text="Register", bg="#FAEBD7",font=("times new roman",20,"bold"),fg="black", width=9, height=1, bd=5,command=insert)
btn.place(x=220, y=470)


def log():
    from subprocess import call
    call(["python","login.py"])
    root.destroy()
    
def window():
  root.destroy()
  
  
def con():
    from subprocess import call
    call(["python","gui main.py"])
    root.destroy()

# def about():
#     from subprocess import call
#     call(["python","aboutus.py"])
#     root.destroy()
    
    
button1 = tk.Button(label_l1, text="HOME", command=con, width=8, height=1,font=('times 15 bold'),bd=0, bg="skyblue", fg="white")
button1.place(x=1210, y=40)

button2 = tk.Button(label_l1, text="LOGIN",command=log,width=8, height=1,font=('times 15 bold'), bd=0,bg="skyblue", fg="white")
button2.place(x=1310, y=40)

button4 = tk.Button(label_l1, text="EXIT", command=window, width=8, height=1,font=('times 15 bold'),bd=0,bg="skyblue", fg="white")
button4.place(x=1400, y=40)





root.mainloop()




# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk
# import sqlite3, re, os, sys

# PALETTE = {'BG': '#0f172a', 'BG_DARK': '#0b1220', 'CARD': '#111827', 'CARD_ALT': '#0b1220', 'TEXT': '#e5e7eb', 'MUTED': '#9ca3af', 'PRIMARY': '#6366f1', 'PRIMARY_HL': '#818cf8', 'ACCENT': '#22d3ee', 'DANGER': '#ef4444', 'SUCCESS': '#10b981'}

# def apply_theme(root: tk.Tk):
#     root.configure(bg=PALETTE["BG"])
#     style = ttk.Style()
#     try:
#         style.theme_use("clam")
#     except:
#         pass
#     style.configure("Title.TLabel", background=PALETTE["BG"], foreground=PALETTE["TEXT"], font=("Segoe UI", 22, "bold"))
#     style.configure("Card.TFrame", background=PALETTE["CARD"])
#     style.configure("TLabel", background=PALETTE["CARD"], foreground=PALETTE["TEXT"])
#     style.configure("Muted.TLabel", background=PALETTE["CARD"], foreground=PALETTE["MUTED"])
#     style.configure("TEntry", fieldbackground=PALETTE["CARD_ALT"], foreground=PALETTE["TEXT"])
#     style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"))
#     style.map("Primary.TButton",
#               background=[("!disabled", PALETTE["PRIMARY"]), ("active", PALETTE["PRIMARY_HL"])],
#               foreground=[("!disabled", "white")])

# class RegisterApp:
#     def __init__(self, root: tk.Tk):
#         self.root = root
#         self.root.title("Create Account • Diabetic Mellitus Detection")
#         self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#         apply_theme(self.root)

#         header = ttk.Frame(self.root)
#         header.pack(fill="x", side="top")
#         ttk.Label(header, text="Create your account", style="Title.TLabel").pack(padx=24, pady=16, side="left")

#         card = ttk.Frame(self.root, style="Card.TFrame", padding=28)
#         card.place(relx=0.5, rely=0.5, anchor="center")
#         inner = card

#         self.Fullname = tk.StringVar()
#         self.address = tk.StringVar()
#         self.username = tk.StringVar()
#         self.Email = tk.StringVar()
#         self.Phoneno = tk.StringVar()
#         self.password = tk.StringVar()
#         self.password1 = tk.StringVar()

#         row = 0
#         ttk.Label(inner, text="Full name").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.Fullname, width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Address").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.address, width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Email").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.Email, width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Phone number").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.Phoneno, width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Username").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.username, width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Password").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.password, show="•", width=36).grid(row=row, column=0, sticky="ew", pady=(0,8)); row+=1

#         ttk.Label(inner, text="Confirm password").grid(row=row, column=0, sticky="w"); row+=1
#         ttk.Entry(inner, textvariable=self.password1, show="•", width=36).grid(row=row, column=0, sticky="ew", pady=(0,12)); row+=1

#         actions = ttk.Frame(inner, style="Card.TFrame")
#         actions.grid(row=row, column=0, sticky="ew")
#         ttk.Button(actions, text="Create account", style="Primary.TButton", command=self.insert).pack(side="left", padx=(0,8))
#         ttk.Button(actions, text="Back to login", command=self.go_login).pack(side="left")

#         self.init_db()

#     def init_db(self):
#         db = sqlite3.connect('evaluation.db')
#         cur = db.cursor()
#         cur.execute("CREATE TABLE IF NOT EXISTS registration (Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, password TEXT)")
#         db.commit()
#         db.close()

#     def password_check(self, pwd: str) -> bool:
#         if len(pwd) < 6 or len(pwd) > 20:
#             return False
#         if not any(ch.isdigit() for ch in pwd):
#             return False
#         if not any(ch.isupper() for ch in pwd):
#             return False
#         if not any(ch.islower() for ch in pwd):
#             return False
#         if not any(ch in "$@#%" for ch in pwd):
#             return False
#         return True

#     def insert(self):
#         fname = self.Fullname.get().strip()
#         addr = self.address.get().strip()
#         un   = self.username.get().strip()
#         email= self.Email.get().strip()
#         mobile = self.Phoneno.get().strip()
#         pwd  = self.password.get()
#         cnpwd= self.password1.get()

#         email_ok = re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+@\w+\.\w{2,3}$', email) is not None

#         if (not fname or fname.isdigit()):
#             messagebox.showinfo("Message", "Please enter a valid full name.")
#             return
#         if not addr:
#             messagebox.showinfo("Message", "Please enter address.")
#             return
#         if not email or not email_ok:
#             messagebox.showinfo("Message", "Please enter a valid email.")
#             return
#         if len(mobile) != 10 or not mobile.isdigit():
#             messagebox.showinfo("Message", "Please enter 10 digit mobile number.")
#             return
#         if not un:
#             messagebox.showinfo("Message", "Please enter username.")
#             return

#         db = sqlite3.connect('evaluation.db')
#         cur = db.cursor()
#         cur.execute("SELECT 1 FROM registration WHERE username=?", (un,))
#         if cur.fetchone():
#             messagebox.showerror("Error!", "Username taken. Try a different one.")
#             db.close()
#             return
#         if not pwd or not self.password_check(pwd):
#             messagebox.showinfo("Message", "Password must contain at least 1 uppercase, 1 lowercase, 1 number and one of $@#%.")
#             db.close()
#             return
#         if pwd != cnpwd:
#             messagebox.showinfo("Message", "Password and Confirm password must match.")
#             db.close()
#             return

#         cur.execute("INSERT INTO registration (Fullname, address, username, Email, Phoneno, password) VALUES (?,?,?,?,?,?)",
#                     (fname, addr, un, email, mobile, pwd))
#         db.commit()
#         db.close()
#         messagebox.showinfo("Success!", "Account created successfully!")
#         self.go_login()

#     def go_login(self):
#         os.system(f"{{sys.executable}} login.py")
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = RegisterApp(root)
#     root.mainloop()
