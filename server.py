import os
import sqlite3
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
try:
    import onnxruntime as ort
except ImportError:
    ort = None
from PIL import Image
import shutil
import time
from datetime import datetime
import gc

app = FastAPI(title="Diabetes Tracker API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load context with absolute paths
MODEL_PATH = os.path.join(BASE_DIR, "model1.onnx")
LABELS_PATH = os.path.join(BASE_DIR, "labels.txt")
DATABASE_PATH = os.path.join(BASE_DIR, "evaluation.db")

# Database Helper
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # User Registration Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration (
            Fullname TEXT, address TEXT, username TEXT, Email TEXT, 
            Phoneno TEXT, Gender TEXT, age TEXT, password TEXT
        )
    """)
    # Analysis History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            prediction TEXT,
            confidence TEXT,
            image_path TEXT,
            date TEXT,
            day TEXT,
            time TEXT
        )
    """)
    # Migration: Try to add time column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE analysis_history ADD COLUMN time TEXT")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

# Initialize ONNX Session
ort_session = None
model_load_error = None

try:
    if not ort:
        model_load_error = "ONNX Runtime library not found."
        print(f"ERROR: {model_load_error}")
    elif os.path.exists(MODEL_PATH):
        # Using CPU for maximum compatibility on Render free tier
        ort_session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        print(f"SUCCESS: ONNX Model loaded from {MODEL_PATH}")
    else:
        model_load_error = f"Model file missing at {MODEL_PATH}"
        print(f"ERROR: {model_load_error}")
except Exception as e:
    model_load_error = str(e)
    print(f"CRITICAL: Error loading ONNX model: {e}")

class_names = []
if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f.readlines()]

# History Endpoints
@app.get("/api/analysis/list")
async def get_analysis_history(username: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM analysis_history WHERE username = ? ORDER BY id DESC", (username,))
    results = cursor.fetchall()
    db.close()
    return {"status": "success", "history": [dict(r) for r in results]}

@app.post("/api/analysis/save")
async def save_analysis(
    username: str = Form(...),
    prediction: str = Form(...),
    confidence: str = Form(...),
    image_path: str = Form(...)
):
    db = get_db()
    cursor = db.cursor()
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    day_str = now.strftime("%A")
    time_str = now.strftime("%H:%M")
    try:
        cursor.execute(
            "INSERT INTO analysis_history (username, prediction, confidence, image_path, date, day, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, prediction, confidence, image_path, date_str, day_str, time_str)
        )
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.delete("/api/analysis/delete/{id}")
async def delete_analysis(id: int):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM analysis_history WHERE id = ?", (id,))
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Auth Endpoints
@app.post("/api/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM registration WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    db.close()
    
    if user:
        return {
            "status": "success", 
            "user": {
                "username": user["username"],
                "fullname": user["Fullname"],
                "email": user["Email"],
                "phone": user["Phoneno"],
                "age": user["age"],
                "address": user["address"],
                "gender": user["Gender"],
                "password": user["password"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/auth/register")
async def register(
    fullname: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    age: str = Form(""),
    address: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    gender: str = Form("Unspecified")
):
    db = get_db()
    cursor = db.cursor()
    try:
        # Check if username exists
        cursor.execute("SELECT * FROM registration WHERE username = ?", (username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        cursor.execute(
            "INSERT INTO registration (Fullname, address, username, Email, Phoneno, Gender, age, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (fullname, address, username, email, phone, gender, age, password)
        )
        db.commit()
        return {"status": "success", "message": "User registered"}
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
@app.post("/api/profile/update")
async def update_profile(
    current_username: str = Form(...),
    fullname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    age: str = Form(...),
    address: str = Form(...),
    password: str = Form(...)
):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE registration SET Fullname=?, Email=?, Phoneno=?, age=?, address=?, password=? WHERE username=?",
            (fullname, email, phone, age, address, password, current_username)
        )
        db.commit()
        return {"status": "success", "message": "Profile updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Config Constants
IMAGE_SIZE = 200
MODEL_IMAGE_SIZE = 64

# Prediction Endpoints
@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    if not ort_session:
        print(f"CRITICAL: ML Model (ONNX) not available: {model_load_error}")
        raise HTTPException(
            status_code=500, 
            detail=f"ML Model not loaded: {model_load_error or 'Unknown initialization failure'}"
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    print(f"DEBUG: Processing analysis for {file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Preprocessing Steps
        print("DEBUG: Stage 1 - Loading with OpenCV")
        img_cv = cv2.imread(file_path)
        if img_cv is None:
            print(f"ERROR: OpenCV could not read {file_path}")
            raise HTTPException(status_code=400, detail="Invalid image file or format")
            
        # 1. Grayscale
        print("DEBUG: Stage 2 - Grayscale conversion")
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray_path = os.path.join(UPLOAD_DIR, "gray_" + file.filename)
        cv2.imwrite(gray_path, gray)
        
        # 2. Threshold
        print("DEBUG: Stage 3 - Thresholding")
        _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        threshold_path = os.path.join(UPLOAD_DIR, "thresh_" + file.filename)
        cv2.imwrite(threshold_path, threshold)
        
        # 3. Model Prediction
        print("DEBUG: Stage 4 - ONNX Inference")
        
        # Pre-inference memory cleanup
        gc.collect()
        
        img = Image.open(file_path).convert("RGB").resize((MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE))
        arr = np.array(img).reshape(1, MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE, 3).astype("float32") / 255.0
        
        try:
            # ONNX dynamic input lookup
            input_name = ort_session.get_inputs()[0].name
            prediction = ort_session.run(None, {input_name: arr})[0]
        except Exception as predict_err:
            print(f"ERROR during ONNX inference: {predict_err}")
            raise HTTPException(status_code=500, detail=f"Model Inference Failed: {str(predict_err)}")

        index = int(np.argmax(prediction))
        confidence = float(prediction[0][index])
        
        class_name = class_names[index][2:].strip() if index < len(class_names) else f"Class {index}"
        diagnosis = "Not At A Risk Of Diabetic" if index == 0 else "At A Risk Of Diabetic"
        
        print(f"DEBUG: Inference success: {diagnosis} ({confidence:.2f})")
        
        # Post-inference memory cleanup
        gc.collect()
        
        return {
            "status": "success",
            "prediction": diagnosis,
            "class": class_name,
            "confidence": f"{confidence:.2f}",
            "visuals": {
                "original": f"/uploads/{file.filename}",
                "gray": f"/uploads/gray_{file.filename}",
                "threshold": f"/uploads/thresh_{file.filename}"
            }
        }
    except Exception as e:
        print(f"CRITICAL ERROR in predict: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Analysis Error: {str(e)}")

# PWA & Root Asset Routes
@app.get("/manifest.json")
async def get_manifest():
    return FileResponse("static/manifest.json")

@app.get("/sw.js")
async def get_sw():
    return FileResponse("static/sw.js")

@app.get("/style.css")
async def get_css():
    return FileResponse("static/style.css")

@app.get("/main.js")
async def get_js():
    return FileResponse("static/main.js")

@app.get("/icon.png")
async def get_icon():
    return FileResponse("static/icon.png")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("static/icon.png")

# Root & Static Serving
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Serve the static directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open("http://localhost:8000")

    Timer(1.5, open_browser).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
