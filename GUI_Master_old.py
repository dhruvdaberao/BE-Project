import os
import smtplib
import subprocess
import sys
import time
from email.message import EmailMessage

import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from keras.models import load_model
from tkinter import messagebox as ms
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from ui_theme import PALETTE, apply_theme, fade_in

IMAGE_SIZE = 200
MODEL_IMAGE_SIZE = 64


class PredictionApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Risk Screening • Diabetes Tracker")
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

        apply_theme(self.root)
        fade_in(self.root)

        self.fn = ""
        self.model = None
        self.class_names = None

        self.result_var = tk.StringVar(value="Select an image to begin.")
        self.conf_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Ready")

        self._build_layout()

    def _build_layout(self) -> None:
        shell = ttk.Frame(self.root, style="Root.TFrame", padding=20)
        shell.pack(fill="both", expand=True)

        header = ttk.Frame(shell, style="Root.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Diabetes Risk Screening", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Modern prediction workspace with streamlined controls.", style="HeroBody.TLabel").pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(shell, style="Root.TFrame")
        body.pack(fill="both", expand=True)

        sidebar = ttk.Frame(body, style="Nav.TFrame", padding=16)
        sidebar.pack(side="left", fill="y", padx=(0, 14))

        ttk.Label(sidebar, text="Actions", style="Subheading.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Button(sidebar, text="Select Image", style="Primary.TButton", command=self.openimage).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="Preprocess", style="Secondary.TButton", command=self.convert_grey).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="CNN Prediction", style="Secondary.TButton", command=self.test_model).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="Precautions", style="Ghost.TButton", command=self.prec).pack(fill="x", pady=(10, 4))
        ttk.Button(sidebar, text="Dashboard", style="Ghost.TButton", command=lambda: self.launch("master_GUI.py")).pack(fill="x", pady=4)
        ttk.Button(sidebar, text="Exit", style="Danger.TButton", command=self.root.destroy).pack(fill="x", pady=(16, 0))

        main = ttk.Frame(body, style="Root.TFrame")
        main.pack(side="left", fill="both", expand=True)

        preview_card = ttk.Frame(main, style="Card.TFrame", padding=16)
        preview_card.pack(fill="x")
        ttk.Label(preview_card, text="Image Pipeline", style="Heading.TLabel").grid(row=0, column=0, columnspan=3, sticky="w")

        self.canvas1 = self._create_image_slot(preview_card, 1, 0, "Original")
        self.canvas2 = self._create_image_slot(preview_card, 1, 1, "Grayscale")
        self.canvas3 = self._create_image_slot(preview_card, 1, 2, "Threshold")

        for col in range(3):
            preview_card.columnconfigure(col, weight=1)

        result = ttk.Frame(main, style="SoftCard.TFrame", padding=16)
        result.pack(fill="x", pady=(12, 0))
        ttk.Label(result, text="Prediction Result", style="Subheading.TLabel").pack(anchor="w")
        ttk.Label(result, textvariable=self.result_var, style="Body.TLabel", wraplength=900, justify="left").pack(anchor="w", pady=(8, 0))
        ttk.Label(result, textvariable=self.conf_var, style="Muted.TLabel").pack(anchor="w", pady=(2, 0))

        status = ttk.Frame(shell, style="Root.TFrame")
        status.pack(fill="x", side="bottom", pady=(10, 0))
        ttk.Label(status, textvariable=self.status_var, style="Muted.TLabel").pack(anchor="w")

    def _create_image_slot(self, parent: ttk.Frame, row: int, col: int, label: str) -> tk.Label:
        slot = ttk.Frame(parent, style="Card.TFrame", padding=10)
        slot.grid(row=row, column=col, sticky="nsew", padx=(0, 12 if col < 2 else 0), pady=(10, 0))
        ttk.Label(slot, text=label, style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        canvas = tk.Label(slot, width=260, height=260, bg=PALETTE["surface_alt"], bd=0)
        canvas.pack(fill="both", expand=True)
        return canvas

    def set_status(self, text: str) -> None:
        self.status_var.set(text)
        self.root.update_idletasks()

    def launch(self, script_name: str) -> None:
        subprocess.call([sys.executable, script_name])
        self.root.destroy()

    def prec(self) -> None:
        subprocess.call([sys.executable, "precautions.py"])

    def _set_image(self, canvas: tk.Label, array_or_image: np.ndarray | Image.Image) -> None:
        image = array_or_image if isinstance(array_or_image, Image.Image) else Image.fromarray(array_or_image)
        image = image.resize((240, 240), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(image)
        canvas.configure(image=imgtk)
        canvas.image = imgtk

    def openimage(self) -> None:
        filename = askopenfilename(
            title="Select image for analysis",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"), ("All Files", "*.*")],
        )
        if not filename:
            return

        self.fn = filename
        img = Image.open(self.fn).convert("RGB")
        self._set_image(self.canvas1, img)
        self.result_var.set("Image selected. Run preprocessing or prediction.")
        self.conf_var.set("")
        self.set_status(f"Loaded: {os.path.basename(self.fn)}")

    def convert_grey(self) -> None:
        if not self.fn:
            ms.showinfo("Info", "Please select an image first.")
            return

        img_cv = cv2.imread(self.fn, 1)
        if img_cv is None:
            ms.showerror("Error", "Unable to load selected image.")
            return

        gs = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
        gs = cv2.resize(gs, (IMAGE_SIZE, IMAGE_SIZE))
        _, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        self._set_image(self.canvas2, gs)
        self._set_image(self.canvas3, threshold)

        self.result_var.set("Preprocessing complete.")
        self.conf_var.set("")
        self.set_status("Image preprocessed")

    def _load_model(self) -> None:
        if self.model is None:
            self.set_status("Loading model...")
            self.model = load_model("model1.h5", compile=False)
            self.class_names = open("labels.txt", "r", encoding="utf-8").readlines()
            self.set_status("Model loaded")

    def test_model(self) -> None:
        if not self.fn:
            ms.showinfo("Info", "Please select an image first.")
            return

        self.set_status("Running prediction...")
        start = time.time()
        self._load_model()

        img = Image.open(self.fn).convert("RGB").resize((MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE))
        arr = np.array(img).reshape(1, MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE, 3).astype("float32") / 255.0

        prediction = self.model.predict(arr, verbose=0)
        index = int(np.argmax(prediction))
        confidence_score = float(prediction[0][index])

        class_name = self.class_names[index][2:].strip() if index < len(self.class_names) else f"Class {index}"
        diagnosis = "Not At A Risk Of Diabetic" if index == 0 else "At A Risk Of Diabetic"

        self.result_var.set(f"Prediction: {diagnosis}  •  Class: {class_name}")
        self.conf_var.set(f"Confidence score: {confidence_score:.2f}")

        elapsed = time.time() - start
        self.set_status(f"Prediction complete in {elapsed:.2f} sec")

        if index != 0:
            self.generate_report(diagnosis, confidence_score)

    def generate_report(self, diagnosis: str, confidence_score: float) -> None:
        report_content = (
            "Patient Diabetic Risk Report\n"
            "=============================\n"
            f"Prediction: {diagnosis}\n"
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

        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Report As",
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(report_content)
            self.send_email_with_report(filepath)
        else:
            self.set_status("Report save cancelled")

    def send_email_with_report(self, filepath: str) -> None:
        sender_email = "svpm5512@gmail.com"
        sender_password = "5512SVPM"
        receiver_email = "srshinde5512@gmail.com,raskarrutvika26@gmail.com"

        msg = EmailMessage()
        msg["Subject"] = "Diabetic Risk Report"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg.set_content("Please find attached the diabetic risk report.")

        with open(filepath, "rb") as file:
            file_data = file.read()
            file_name = os.path.basename(filepath)
            msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            self.set_status("Report emailed successfully")
        except Exception:
            self.set_status("Failed to send email report")


if __name__ == "__main__":
    app_root = tk.Tk()
    PredictionApp(app_root)
    app_root.mainloop()
