import requests
import os

url = "http://localhost:8000/api/predict"
image_path = r"C:\Users\dhruv\OneDrive\Desktop\SR_BE_Project\ThermoDataBase\val\0\CG001_M_L.png"

if not os.path.exists(image_path):
    print(f"Test image not found: {image_path}")
    exit(1)

with open(image_path, "rb") as f:
    files = {"file": (os.path.basename(image_path), f, "image/png")}
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.json())
    except Exception as e:
        print(f"Request failed: {e}")
