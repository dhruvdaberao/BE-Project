# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:57:59 2025

@author: HP
"""

import tkinter as tk
from tkinter import messagebox

def show_precautions():
    # Retrieve patient details
    name = name_entry.get()
    age = age_entry.get()

    if not name or not age:
        messagebox.showerror("Error", "Please enter both name and age!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a numeric value!")
        return

    # Precautions text
    precautions = (
        f"Precautions for {name} (Age: {age}):\n\n"
        "1. Regularly monitor blood sugar levels.\n"
        "2. Follow a balanced, low-GI diet.\n"
        "3. Engage in regular physical activity (consult a doctor).\n"
        "4. Take medications or insulin as prescribed.\n"
        "5. Schedule regular health checkups (e.g., HbA1c, eye exams).\n"
        "6. Practice good foot care (inspect feet daily).\n"
        "7. Manage stress through relaxation techniques.\n"
        "8. Avoid smoking and excessive alcohol consumption.\n"
        "9. Be prepared for emergencies (carry glucose tablets or snacks).\n"
        "10. Educate yourself about diabetes management.\n"
    )

    # Create a new window to display precautions
    precautions_window = tk.Toplevel(root)
    precautions_window.title("Precautions for Diabetic Patients")

    precautions_label = tk.Label(precautions_window, text=precautions, justify="left", padx=10, pady=10, font=("Arial", 12))
    precautions_label.pack(fill="both", expand=True, padx=10, pady=10)

    close_button = tk.Button(precautions_window, text="Close", command=precautions_window.destroy)
    close_button.pack(pady=10)

# Main Tkinter Window
root = tk.Tk()
root.title("Diabetic Precautions Generator")

# Input Frame
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Enter Patient Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(frame, width=30, font=("Arial", 12))
name_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Enter Patient Age:", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
age_entry = tk.Entry(frame, width=30, font=("Arial", 12))
age_entry.grid(row=1, column=1, pady=5)

generate_button = tk.Button(root, text="Generate Precautions", command=show_precautions, font=("Arial", 12), padx=10, pady=5)
generate_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()