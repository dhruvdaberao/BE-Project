import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import CNNModel 
from tkinter.filedialog import asksaveasfilename
import smtplib
from email.message import EmailMessage
import os
#from tkvideo import tkvideo

#import tfModel_test as tf_test
global fn
fn=""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="seashell2")
root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Home Page")




# #####For background Image
image2 = Image.open('11.jpg')
image2 = image2.resize((1290, 790), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=250, y=1)  # , relwidth=1, relheight=1)





lbl = tk.Label(root, text="Diabetic Mellitus Detection System", font=('times', 30,' bold '), width=70,height=2,bg="#B0E0E6",fg="black")
lbl.place(x=0, y=0)


frame_alpr = tk.LabelFrame(root, text=" --Process-- ", width=262, height=760, bd=5, font=('times', 14, ' bold '),bg="grey")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=2, y=94)


    
###########################################################################
def train_model():
 
    update_label("Model Training Start...............")
    
    start = time.time()

    X= CNNModel.main()
    
    end = time.time()
        
    ET="Execution Time: {0:.4} seconds \n".format(end-start)
    
    msg="Model Training Completed.."+'\n'+ X + '\n'+ ET

    print(msg)

import functools
import operator


def convert_str_to_tuple(tup):
    s = functools.reduce(operator.add, (tup))
    return s

def test_model_proc(fn):
    from keras.models import load_model
#    from keras.optimizers import Adam

#    global fn
    
    IMAGE_SIZE = 64
    LEARN_RATE = 1.0e-4
    CH=3
    print(fn)
    if fn!="":
        # Model Architecture and Compilation
       
        #model = load_model('ocular_disease.h5')
            
        # adam = Adam(lr=LEARN_RATE, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
        # model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
        # Load the model
        model = load_model("model1.h5", compile=False)
        
        # Load the labels
        class_names = open("labels.txt", "r").readlines()
        
        img = Image.open(fn)
        img = img.resize((IMAGE_SIZE,IMAGE_SIZE))
        img = np.array(img)
        
        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)
        
        img = img.astype('float32')
        img = img / 255.0
        print('img shape:',img)
        
        
        # Predicts the model
        prediction = model.predict(img)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        
        # # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        # print("Confidence Score:", confidence_score)
        
        
        
        if index == 0:
            Cd="Not At A Risk Of Diabetic"
        else:
            Cd="At A Risk Of Diabetic"
        
       
        A=Cd
        
    if index != 0:
            report_content = (
                "Patient Diabetic Risk Report\n"
                "=============================\n"
                f"Prediction: {A}\n"
                f"Confidence Score: {confidence_score:.2f}\n\n"
                "Precautions:\n"
                "1. Regularly monitor blood sugar levels.\n"
                "2. Take medications or insulin as prescribed.\n"
                "3. Maintain proper hydration.\n"
                "4. Practice good foot care.\n"
                "5. Avoid smoking and alcohol consumption.\n\n"
                "Sample Diet Plan:\n"
                "- Breakfast: Whole grain toast, boiled eggs, and a small fruit.\n"
                "- Lunch: Grilled chicken, steamed vegetables, and quinoa.\n"
                "- Snack: Handful of nuts or yogurt.\n"
                "- Dinner: Baked fish, salad, and a small serving of brown rice.\n"
                "- Avoid sugary drinks and processed foods.\n\n"
                "Recommended Actions:\n"
                "- Consult a healthcare provider immediately.\n"
                "- Schedule a follow-up appointment for further testing.\n"
                "- Engage in regular physical activity (e.g., walking, yoga).\n"
            )

            # Ask user for the report save location
            filepath = asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Save Report As"
            )
            if filepath:
                with open(filepath, "w") as file:
                    file.write(report_content)
                print("Report saved successfully!")
                send_email_with_report(filepath)
            else:
                print("Report generation canceled.")
        
        # Return the diagnosis
        
    return A

def send_email_with_report(filepath):
    import smtplib
    from email.message import EmailMessage

    # Configure your email credentials
    sender_email = "svpm5512@gmail.com"  # Replace with your email
    sender_password = "5512SVPM"
    RECEIVER_EMAIL = "srshinde5512@gmail.com,raskarrutvika26@gmail.com"       # Replace with your email password

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = "Diabetic Risk Report"
    msg['From'] = sender_email
    msg['To'] = RECEIVER_EMAIL

    # Email body
    msg.set_content("Please find attached the diabetic risk report.")

    # Attach the report file
    with open(filepath, "rb") as file:
        file_data = file.read()
        file_name = os.path.basename(filepath)
        msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)



def update_label(str_T):
    #clear_img()
    result_label = tk.Label(root, text=str_T, width=40, font=("bold", 25), bg='goldenrod', fg='black')
    result_label.place(x=300, y=450)
# def train_model():
    
#     update_label("Model Training Start...............")
    
#     start = time.time()

#     X=Model_frm.main()
    
#     end = time.time()
        
#     ET="Execution Time: {0:.4} seconds \n".format(end-start)
    
#     msg="Model Training Completed.."+'\n'+ X + '\n'+ ET

#     update_label(msg)

def test_model():
    global fn
    if fn!="":
        update_label("Model Testing Start...............")
        
        start = time.time()
    
        X=test_model_proc(fn)
        
        X1="Selected Image is {0}".format(X)
        
        end = time.time()
            
        ET="Execution Time: {0:.4} seconds \n".format(end-start)
        
        msg="Image Testing Completed.."+'\n'+ X1 + '\n'+ ET
        fn=""
        
    else:
        msg="Please Select Image For Prediction...."
        
    update_label(msg)
    
    
def openimage():
   
    global fn
    fileName = askopenfilename(initialdir='E:/Dibetes Mellitus', title='Select image for Aanalysis ',
                               filetypes=[("all files", "*.*")])
    IMAGE_SIZE=200
    imgpath = fileName
    fn = fileName


#        img = Image.open(imgpath).convert("L")
    img = Image.open(imgpath)
    
    img = img.resize((IMAGE_SIZE,200))
    img = np.array(img)
#        img = img / 255.0
#        img = img.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)


    x1 = int(img.shape[0])
    y1 = int(img.shape[1])


#
#        gs = cv2.cvtColor(cv2.imread(imgpath, 1), cv2.COLOR_RGB2GRAY)
#
#        gs = cv2.resize(gs, (x1, y1))
#
#        retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(im)
    img = tk.Label(root, image=imgtk, height=250, width=250)
    
    #result_label1 = tk.Label(root, image=imgtk, width=250,height=250)
    #result_label1.place(x=300, y=100)
    img.image = imgtk
    img.place(x=300, y=100)
   # out_label.config(text=imgpath)

def convert_grey():
    global fn    
    IMAGE_SIZE=200
    
    img = Image.open(fn)
    img = img.resize((IMAGE_SIZE,200))
    img = np.array(img)
    
    x1 = int(img.shape[0])
    y1 = int(img.shape[1])

    gs = cv2.cvtColor(cv2.imread(fn, 1), cv2.COLOR_RGB2GRAY)

    gs = cv2.resize(gs, (x1, y1))

    retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(threshold)

    im = Image.fromarray(gs)
    imgtk = ImageTk.PhotoImage(image=im)
    
    #result_label1 = tk.Label(root, image=imgtk, width=250, font=("bold", 25), bg='bisque2', fg='black',height=250)
    #result_label1.place(x=300, y=400)
    img2 = tk.Label(root, image=imgtk, height=250, width=250,bg='white')
    img2.image = imgtk
    img2.place(x=580, y=100)

    im = Image.fromarray(threshold)
    imgtk = ImageTk.PhotoImage(image=im)

    img3 = tk.Label(root, image=imgtk, height=250, width=250)
    img3.image = imgtk
    img3.place(x=880, y=100)
    #result_label1 = tk.Label(root, image=imgtk, width=250,height=250, font=("bold", 25), bg='bisque2', fg='black')
    #result_label1.place(x=300, y=400)



def prec():
    from subprocess import call
    call(["python","precautions.py"])
def window():
    root.destroy()
from tkinter import messagebox as ms


button1 = tk.Button(frame_alpr, text=" Select_Image ", command=openimage,width=15, height=1, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
button1.place(x=30, y=100)

button2 = tk.Button(frame_alpr, text="Image_preprocess", command=convert_grey, width=15, height=1, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
button2.place(x=30, y=200)

# # 
button4 = tk.Button(frame_alpr, text="CNN_Prediction", command=test_model,width=15, height=1,bg="#B0E0E6",fg="black", font=('times', 15, ' bold '))
button4.place(x=30, y=300)
button4 = tk.Button(frame_alpr, text="Precaution", command=prec,width=15, height=1,bg="#B0E0E6",fg="black", font=('times', 15, ' bold '))
button4.place(x=30, y=400)


# button3 = tk.Button(frame_alpr, text="Train Model", command=train_model, width=15, height=1, font=('times', 15, ' bold '),bg="#B0E0E6",fg="black")
# button3.place(x=30, y=400)

# button5 = tk.Button(root, text="ULCER", command=window,width=8, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
# button5.place(x=450, y=250)

# button5 = tk.Button(root, text="DIBETES MELLITUS", command=window,width=18, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
# button5.place(x=750, y=350)

#
#button5 = tk.Button(frame_alpr, text="button5", command=window,width=8, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
#button5.place(x=450, y=20)


exit = tk.Button(frame_alpr, text="Exit", command=window, width=15, height=1,bg="red", font=('times', 15, ' bold '),fg="white")
exit.place(x=30, y=500)



root.mainloop()



# import tkinter as tk
# from tkinter import ttk
# from tkinter.filedialog import askopenfilename, asksaveasfilename
# from tkinter import messagebox as ms
# from PIL import Image, ImageTk
# import numpy as np
# import cv2, time, os, sys
# from keras.models import load_model
# try:
#     import CNNModel
# except Exception:
#     CNNModel = None
# PALETTE = {'BG': '#0f172a', 'BG_DARK': '#0b1220', 'CARD': '#111827', 'CARD_ALT': '#0b1220', 'TEXT': '#e5e7eb', 'MUTED': '#9ca3af', 'PRIMARY': '#6366f1', 'PRIMARY_HL': '#818cf8', 'ACCENT': '#22d3ee', 'DANGER': '#ef4444', 'SUCCESS': '#10b981'}


# def apply_theme(root):
#     style = ttk.Style()
#     try:
#         style.theme_use("clam")
#     except:
#         pass
#     root.configure(bg=PALETTE["BG"])
#     style.configure("Title.TLabel", background=PALETTE["BG"], foreground=PALETTE["TEXT"], font=("Segoe UI", 22, "bold"))
#     style.configure("Sub.TLabel", background=PALETTE["BG"], foreground=PALETTE["MUTED"], font=("Segoe UI", 11))
#     style.configure("Card.TFrame", background=PALETTE["CARD"])
#     style.configure("Nav.TFrame", background=PALETTE["BG"])
#     style.configure("Muted.TLabel", background=PALETTE["CARD"], foreground=PALETTE["MUTED"])
#     style.configure("TLabel", background=PALETTE["CARD"], foreground=PALETTE["TEXT"])
#     style.configure("TEntry", fieldbackground=PALETTE["CARD_ALT"], foreground=PALETTE["TEXT"])
#     style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=10)
#     style.map("Primary.TButton",
#               background=[("!disabled", PALETTE["PRIMARY"]), ("active", PALETTE["PRIMARY_HL"])],
#               foreground=[("!disabled", "white")])
#     style.configure("TButton", padding=10)
#     style.map("TButton",
#               background=[("active", PALETTE["CARD_ALT"])],
#               foreground=[("!disabled", PALETTE["TEXT"])])


#     IMAGE_SIZE = 64

#     class PredictApp:
#         def __init__(self, root: tk.Tk):
#             self.root = root
#             self.root.title("Detection • Diabetic Mellitus")
#             self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
#             apply_theme(self.root)

#             self.fn = ""
#             self.result_var = tk.StringVar(value="Select an image to begin.")
#             self.conf_var = tk.StringVar(value="")
#             self.status_var = tk.StringVar(value="Ready")

#             header = ttk.Frame(self.root, style="Nav.TFrame")
#             header.pack(fill="x")
#             ttk.Label(header, text="Diabetic Mellitus Detection System", style="Title.TLabel").pack(anchor="w", padx=24, pady=(16,0))
#             ttk.Label(header, text="Model inference and utilities", style="Sub.TLabel").pack(anchor="w", padx=24, pady=(0,12))

#             body = ttk.Frame(self.root, style="Nav.TFrame")
#             body.pack(fill="both", expand=True)

#             sidebar = ttk.Frame(body, style="Card.TFrame", padding=16)
#             sidebar.pack(side="left", fill="y", padx=16, pady=16)

#             ttk.Button(sidebar, text="Select Image", style="Primary.TButton", command=self.openimage).pack(fill="x", pady=(0,8))
#             ttk.Button(sidebar, text="Image Preprocess", command=self.convert_grey).pack(fill="x", pady=4)
#             ttk.Button(sidebar, text="CNN Prediction", command=self.test_model).pack(fill="x", pady=4)
#             ttk.Button(sidebar, text="Precautions", command=self.open_precautions).pack(fill="x", pady=4)
#             ttk.Button(sidebar, text="Back to Home", command=lambda: self.launch("master_GUI.py")).pack(fill="x", pady=(16,4))
#             ttk.Button(sidebar, text="Exit", command=self.root.destroy).pack(fill="x", pady=4)

#             content = ttk.Frame(body, style="Nav.TFrame")
#             content.pack(side="left", fill="both", expand=True, padx=(0,16), pady=16)

#             preview = ttk.Frame(content, style="Card.TFrame", padding=16)
#             preview.pack(fill="x")
#             self.img_label1 = ttk.Label(preview, text="Original", style="Muted.TLabel")
#             self.img_label2 = ttk.Label(preview, text="Grayscale", style="Muted.TLabel")
#             self.img_label3 = ttk.Label(preview, text="Threshold", style="Muted.TLabel")
#             self.img_label1.grid(row=0, column=0, sticky="w")
#             self.img_label2.grid(row=0, column=1, sticky="w", padx=12)
#             self.img_label3.grid(row=0, column=2, sticky="w")

#             self.canvas1 = tk.Label(preview, bg=PALETTE["CARD"], width=250, height=250)
#             self.canvas2 = tk.Label(preview, bg=PALETTE["CARD"], width=250, height=250)
#             self.canvas3 = tk.Label(preview, bg=PALETTE["CARD"], width=250, height=250)
#             self.canvas1.grid(row=1, column=0, pady=8)
#             self.canvas2.grid(row=1, column=1, padx=12, pady=8)
#             self.canvas3.grid(row=1, column=2, pady=8)

#             result_card = ttk.Frame(content, style="Card.TFrame", padding=16)
#             result_card.pack(fill="x", pady=(12,0))
#             ttk.Label(result_card, text="Result", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")
#             ttk.Label(result_card, textvariable=self.result_var).grid(row=1, column=0, sticky="w", pady=(6,0))
#             ttk.Label(result_card, textvariable=self.conf_var, style="Muted.TLabel").grid(row=2, column=0, sticky="w")

#             status = ttk.Frame(self.root, style="Nav.TFrame")
#             status.pack(fill="x", side="bottom")
#             ttk.Label(status, textvariable=self.status_var, style="Sub.TLabel").pack(anchor="w", padx=16, pady=8)

#             self.model = None
#             self.labels = None

#         def set_status(self, text):
#             self.status_var.set(text)
#             self.root.update_idletasks()

#         def launch(self, filename):
#             os.system(f"{sys.executable} {filename}")
#             self.root.destroy()

#         def open_precautions(self):
#             os.system(f"{sys.executable} precautions.py")

#         def openimage(self):
#             fileName = askopenfilename(title='Select image for analysis',
#                                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")])
#             if not fileName:
#                 return
#             self.fn = fileName
#             IMAGE_SIZE = 200

#             img = Image.open(self.fn).resize((IMAGE_SIZE, IMAGE_SIZE))
#             imgtk = ImageTk.PhotoImage(img)
#             self.canvas1.configure(image=imgtk)
#             self.canvas1.image = imgtk

#             self.result_var.set("Image selected. You can preprocess or run prediction.")
#             self.conf_var.set("")

#         def convert_grey(self):
#             if not self.fn:
#                 ms.showinfo("Info", "Please select an image first.")
#                 return
#             IMAGE_SIZE = 200

#             gs = cv2.cvtColor(cv2.imread(self.fn, 1), cv2.COLOR_RGB2GRAY)
#             gs = cv2.resize(gs, (IMAGE_SIZE, IMAGE_SIZE))
#             _, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

#             img_gs = Image.fromarray(gs)
#             img_thr = Image.fromarray(threshold)

#             imgtk_gs = ImageTk.PhotoImage(img_gs)
#             imgtk_thr = ImageTk.PhotoImage(img_thr)

#             self.canvas2.configure(image=imgtk_gs)
#             self.canvas2.image = imgtk_gs

#             self.canvas3.configure(image=imgtk_thr)
#             self.canvas3.image = imgtk_thr

#             self.result_var.set("Preprocessing complete.")
#             self.conf_var.set("")

#         def _load_model_and_labels(self):
#             if self.model is None:
#                 self.set_status("Loading model...")
#                 self.model = load_model("model1.h5", compile=False)
#                 with open("labels.txt", "r") as f:
#                     self.labels = [line.strip() for line in f.readlines()]
#                 self.set_status("Model loaded.")
#             return self.model, self.labels

#         def test_model(self):
#             if not self.fn:
#                 ms.showinfo("Info", "Please select an image first.")
#                 return

#             self.set_status("Predicting...")
#             model, labels = self._load_model_and_labels()

#             img = Image.open(self.fn).resize((IMAGE_SIZE, IMAGE_SIZE))
#             arr = np.array(img).reshape(1, IMAGE_SIZE, IMAGE_SIZE, 3).astype("float32") / 255.0

#             pred = model.predict(arr)
#             idx = int(np.argmax(pred))
#             class_name = labels[idx] if idx < len(labels) else f"Class {idx}"
#             confidence = float(pred[0][idx])

#             diagnosis = "Not At A Risk Of Diabetic" if idx == 0 else "At A Risk Of Diabetic"

#             self.result_var.set(f"Prediction: {diagnosis}  •  Class: {class_name}")
#             self.conf_var.set(f"Confidence: {confidence:.2f}")
#             self.set_status("Prediction complete.")

#             if idx != 0:
#                 self.generate_report(diagnosis, confidence)

#         def generate_report(self, diagnosis, confidence):
#             report = (
#                 "Patient Diabetic Risk Report\n"
#                 "=============================\n"
#                 f"Prediction: {diagnosis}\n"
#                 f"Confidence Score: {confidence:.2f}\n\n"
#                 "Precautions:\n"
#                 "1. Regularly monitor blood sugar levels.\n"
#                 "2. Take medications or insulin as prescribed.\n"
#                 "3. Maintain proper hydration.\n"
#                 "4. Practice good foot care.\n"
#                 "5. Avoid smoking and alcohol consumption.\n\n"
#                 "Sample Diet Plan:\n"
#                 "- Breakfast: Whole grain toast, boiled eggs, and a small fruit.\n"
#                 "- Lunch: Grilled protein, steamed vegetables, and quinoa.\n"
#                 "- Snack: Handful of nuts or yogurt.\n"
#                 "- Dinner: Baked fish/legumes, salad, and brown rice.\n"
#                 "- Avoid sugary drinks and processed foods.\n\n"
#                 "Recommended Actions:\n"
#                 "- Consult a healthcare provider immediately.\n"
#                 "- Schedule a follow-up appointment for further testing.\n"
#                 "- Engage in regular physical activity (e.g., walking, yoga).\n"
#             )
#             filepath = asksaveasfilename(defaultextension=".txt",
#                                          filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
#                                          title="Save Report As")
#             if filepath:
#                 with open(filepath, "w") as f:
#                     f.write(report)
#                 ms.showinfo("Saved", "Report saved successfully.")
#             else:
#                 self.set_status("Report generation canceled.")

#     if __name__ == "__main__":
#         root = tk.Tk()
#         app = PredictApp(root)
#         root.mainloop()
