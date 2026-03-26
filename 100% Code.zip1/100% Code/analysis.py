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
root.title("Master Page")

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 = Image.open('6.webp')
image2 = image2.resize((w,h), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)




label_l1 = tk.Label(root, text=" Analysis Of The Region That Might Spread The Disease.",font=("Times New Roman", 30, 'bold'),
                    background="skyblue", fg="white", width=67, height=2)
label_l1.place(x=0, y=0)

img = Image.open('7.png')
img = img.resize((100,70), Image.ANTIALIAS)
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


# frame_alpr = tk.LabelFrame(root, text=" --Register-- ", width=700, height=700, bd=5, font=('times', 14, ' bold '),fg="white",bg="gray")
# frame_alpr.grid(row=0, column=0, sticky='nw')
# frame_alpr.place(x=0, y=98)

Login_frame=tk.Frame(root)
Login_frame.place(x=50,y=200)
        
logolbl=tk.Label(Login_frame,bd=0).grid(row=0,columnspan=2,pady=20)
        
lbluser=tk.Label(Login_frame,text=" || Analysis of Disease Spread || \n 1.Post-Processing\n After detecting ulcers, post-process the results to analyze the spread or severity of the disease.\n  Measure the size and distribution of ulcer regions within the images.\n 2.Quantitative Metrics\n Develop metrics to quantify the extent of disease spread, such as the percentage of affected area or the number of ulcers.\n 3.Clinical Validation\n Collaborate with medical professionals to validate the model's findings clinically.\n Ensure that the model's predictions align with real-world disease progression.",font=("Times new roman", 20, "bold"),bg="white").grid(row=1,column=0,padx=20,pady=10)



    
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
    
    
# button1 = tk.Button(label_l1, text="HOME", command=con, width=8, height=1,font=('times 15 bold'),bd=0, bg="skyblue", fg="white")
# button1.place(x=1210, y=40)

# button2 = tk.Button(label_l1, text="LOGIN",command=log,width=8, height=1,font=('times 15 bold'), bd=0,bg="skyblue", fg="white")
# button2.place(x=1310, y=40)

# button4 = tk.Button(label_l1, text="EXIT", command=window, width=8, height=1,font=('times 15 bold'),bd=0,bg="skyblue", fg="white")
# button4.place(x=1400, y=40)





root.mainloop()