
from tkinter import *
import tkinter as tk
from PIL import Image ,ImageTk
from tkinter.ttk import *
from pymsgbox import *


root = tk.Tk()
root.configure(background="white")
# root.geometry("1300x700")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("HOME")
# bg = Image.open(r"y11.jpg")
# bg.resize((w,h),Image.ANTIALIAS)
# print(w,h)
# bg_img = ImageTk.PhotoImage(bg)
# bg_lbl = tk.Label(root,image=bg_img)
# #bg_lbl.bg_img
# bg_lbl.place(x=0,y=93)
# #, relwidth=1, relheight=1)
# label_l1 = tk.Label(root, text="CYBER BULLYING USING TWITTER",font=("Times New Roman", 35, 'bold'),
#                     background="black", fg="white", width=60, height=1)
# label_l1.place(x=0, y=0)



img=ImageTk.PhotoImage(Image.open("1.jpg"))

img2=ImageTk.PhotoImage(Image.open("2.png"))

img3=ImageTk.PhotoImage(Image.open("3.jpg"))


logo_label=tk.Label()
logo_label.place(x=0,y=0)



# using recursion to slide to next image

x = 1

# function to change to next image
def move():
	global x
	if x == 4:
		x = 1
	if x == 1:
		logo_label.config(image=img)
	elif x == 2:
		logo_label.config(image=img2)
	elif x == 3:
		logo_label.config(image=img3)
	x = x+1
	root.after(2000, move)

# calling the function
move()
#

#marquee
def shift():
    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): #reset the coordinates
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

canvas=Canvas(root,bg="black")
canvas.pack()
text_var=" Diabetic Mellitus Using Foot Thermography"
text=canvas.create_text(0,-2000,text=text_var,font=('Raleway',25,'bold'),fill='white',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = 1600
height = 100
canvas['width']=width
canvas['height']=height
fps=40    #Change the fps to make the animation faster/slower
shift()   #Function Calling


'''
def marquee_fun(widget, widget_w, widget_h, total_w, total_h, direction, speed, position=0):
    if direction=='right':
        if position>=total_w-widget_w:
            position=0
        position = position + speed
        widget.place(x=position)
        
    widget.after(10, lambda: marquee_fun(widget, widget_w, widget_h, total_w, total_h, direction, speed))

w = tk.Label(root, text="Crop Prediction Using Machine Learning",background="#17202A",foreground="white",font=("Times new roman",19,"bold"))
w.place(x=0,y=15, width=150, height=30)


w.after(100, lambda:marquee_fun(w, 150, 30, 500, 500, 'right', 2))

'''


def Login():
    from subprocess import call
    call(["python","login.py"])
def Register():
    from subprocess import call
    call(["python","register.py"])

def window():
    root.destroy()



button1 = tk.Button(root, text="Login", command=Login, width=12, height=2,bd=5,font=('times', 20, ' bold '), bg="gray", fg="white")
button1.place(x=400, y=650)

button2 = tk.Button(root, text="Register",command=Register,width=12, height=2,bd=5,font=('times', 20, ' bold '), bg="gray", fg="white")
button2.place(x=700, y=650)

button3 = tk.Button(root, text="Exit",command=window,width=12, height=2,bd=5,font=('times', 20, ' bold '), bg="red", fg="white")
button3.place(x=1000, y=650)



root.mainloop()




# import tkinter as tk
# from tkinter import ttk
# import os
# import sys

# PALETTE = {
#     "BG": "#0f172a",
#     "BG_DARK": "#0b1220",
#     "CARD": "#111827",
#     "CARD_ALT": "#0b1220",
#     "TEXT": "#e5e7eb",
#     "MUTED": "#9ca3af",
#     "PRIMARY": "#6366f1",
#     "PRIMARY_HL": "#818cf8",
#     "ACCENT": "#22d3ee",
#     "DANGER": "#ef4444",
#     "SUCCESS": "#10b981",
# }

# def apply_theme(root):
#     style = ttk.Style()
#     try:
#         style.theme_use("clam")
#     except:
#         pass

#     root.configure(bg=PALETTE["BG"])

#     style.configure("Title.TLabel", background=PALETTE["BG"],
#                     foreground=PALETTE["TEXT"], font=("Segoe UI", 22, "bold"))
#     style.configure("Sub.TLabel", background=PALETTE["BG"],
#                     foreground=PALETTE["MUTED"], font=("Segoe UI", 11))
#     style.configure("Card.TFrame", background=PALETTE["CARD"])
#     style.configure("Nav.TFrame", background=PALETTE["BG"])
    
#     style.configure("TLabel", background=PALETTE["CARD"], foreground=PALETTE["TEXT"])
#     style.configure("Muted.TLabel", background=PALETTE["CARD"], foreground=PALETTE["MUTED"])

#     style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=10)
#     style.map("Primary.TButton",
#               background=[("!disabled", PALETTE["PRIMARY"]),
#                           ("active", PALETTE["PRIMARY_HL"])],
#               foreground=[("!disabled", "white")])

#     style.configure("TButton", padding=10)
#     style.map("TButton",
#               background=[("active", PALETTE["CARD_ALT"])],
#               foreground=[("!disabled", PALETTE["TEXT"])])


# class LandingApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Welcome • Diabetic Mellitus Detection")
#         self.root.geometry("900x600")
#         apply_theme(self.root)

#         # -----------------------------------------
#         # HEADER (safe)
#         # -----------------------------------------
#         header = ttk.Frame(self.root, style="Nav.TFrame", padding=20)
#         header.pack(fill="x")

#         ttk.Label(header,
#                   text="Diabetic Mellitus Using Foot Thermography",
#                   style="Title.TLabel").pack(anchor="w")

#         ttk.Label(header,
#                   text="Modern UI • Theme #5",
#                   style="Sub.TLabel").pack(anchor="w")

#         # -----------------------------------------
#         # MAIN CONTENT
#         # -----------------------------------------
#         card = ttk.Frame(self.root, style="Card.TFrame", padding=40)
#         card.pack(pady=60)

#         ttk.Label(card, text="Detect early. Act confidently.",
#                   font=("Segoe UI", 20, "bold")).pack(anchor="w")

#         ttk.Label(card, text="Sign in or create an account to continue",
#                   style="Muted.TLabel").pack(anchor="w", pady=(0, 20))

#         actions = ttk.Frame(card, style="Card.TFrame")
#         actions.pack(anchor="w")

#         ttk.Button(actions, text="Login", style="Primary.TButton",
#                    command=lambda: self.launch("login.py")).pack(side="left", padx=(0, 10))

#         ttk.Button(actions, text="Register",
#                    command=lambda: self.launch("register.py")).pack(side="left")

#         # -----------------------------------------
#         # FOOTER
#         # -----------------------------------------
#         footer = ttk.Frame(self.root, style="Nav.TFrame", padding=10)
#         footer.pack(side="bottom", fill="x")

#         ttk.Button(footer, text="Exit", command=self.root.destroy).pack(side="right", padx=10)


#     def launch(self, filename):
#         os.system(f"{sys.executable} {filename}")
#         self.root.destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LandingApp(root)
#     root.mainloop()

