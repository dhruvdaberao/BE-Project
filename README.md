# Diabetes Tracker: Non-Invasive Diabetic Risk & Neuropathy Assessment

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX--Runtime-1.14%2B-005C99.svg?style=flat&logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, non-invasive screening platform designed for early detection of **Diabetic Neuropathy** and pre-ulcerative diabetic foot risk. By combining **plantar thermography (infrared thermal imaging)**, multi-stage computer vision preprocessing, and an optimized **Convolutional Neural Network (CNN)** executed via **ONNX Runtime**, this application provides instant diagnostic analysis directly on desktop and mobile devices.

---

## 🚀 Live Demo & Links

* **GitHub Repository:** [https://github.com/dhruvdaberao/BE-Project.git](https://github.com/dhruvdaberao/BE-Project.git)
* **Live Hosted Application:** [https://be-project.onrender.com](https://be-project.onrender.com) *(Hosted on Render)*
* **Execution & Deployment Guide:** [deployment.md](file:///C:/Users/dhruv/OneDrive/Desktop/PROJECTS/SR_BE_Project/deployment.md)
* **Comprehensive Project Report:** [Report.md](file:///C:/Users/dhruv/OneDrive/Desktop/PROJECTS/SR_BE_Project/Report.md)

---

## 🌟 Key Features

1. **Plantar Thermogram AI Classification**: Classifies infrared thermal plantar footprints into **Control Group (Normal/Healthy)** vs. **Diabetic Risk Group (Abnormal/Hyperthermic Inflammation)**.
2. **Clinical Color Space Filtering (HSV Heuristic)**: Automatically screens and rejects normal photos (e.g., selfies, objects) by evaluating hue distribution against medical thermal camera palettes (Ironbow/Jet), preventing false diagnoses.
3. **Multi-Stage Visual Segmentation**: 
   * **Grayscale Conversion**: Isolates thermal radiance intensity.
   * **Otsu’s Inverse Binary Thresholding**: Automatically highlights and segments focal hyperthermic hotspots (inflammatory regions) against cooler tissues for easy podiatric review.
4. **Cloud Memory Optimization**: Running the CNN model via **ONNX Runtime** instead of TensorFlow reduces memory usage by **over 70%** (down to `<140MB` RAM) and guarantees sub-100ms inference times on lightweight free-tier cloud servers (Render.com) without OOM crashes.
5. **Interactive Medical Dashboard**: 
   * Responsive layout supporting mobile screens down to **380px**.
   * Secure user registration, multi-criteria login (Username, Email, or Phone), and profile management.
   * Patient diagnostic history log utilizing ACID-compliant embedded **SQLite3**.
   * Graphical health trends and line charts using **Chart.js**.
   * One-click **Clinical Grade PDF Report** export using **html2pdf.js**.
6. **Cross-Platform Progressive Web App (PWA)**: Implements offline caching, instant loading, and standalone app installs across Android, iOS, and Windows.
7. **Legacy Desktop Interface**: Legacy **Tkinter-based GUI** (`gui_main.py`) preserved for offline desktop kiosk deployment.

---

## 📐 System Architecture & Data Pipeline

```
[Client / PWA Dashboard]
        │
        ▼ (Uploads Footprint Scan via POST /api/predict)
[Sanitization & Security Gate]
        │ (Sanitizes filename with timestamp prefix to prevent browser caching)
        ▼
[HSV Color Space Heuristic Filter]
        ├─── [Reject Photo] ───> (HTTP 400 Bad Request Error: Invalid Thermal Image)
        │
        ▼ (If Valid Thermal Image)
[OpenCV Preprocessing Engine]
        ├─── Grayscale Conversion (cv2.cvtColor) ───> Saves gray_*.png
        └─── Otsu's Inverse Thresholding (cv2.threshold) ───> Saves thresh_*.png
        │
        ▼ (Normalized Array Resized to 64x64x3)
[ONNX Inference Engine]
        │ (Runs forward inference via CPUExecutionProvider)
        ▼
[SQLite3 Persistence Log]
        │ (Writes username, prediction, confidence, file paths, date, day, time to evaluation.db)
        ▼
[Dashboard Presentation & PDF Report Export]
```

---

## 🧠 Dataset & Deep Learning Model Details

* **Dataset Size**: **1,444 verified thermal plantar images** (720 Control/Normal footprints, 724 Diabetic/Abnormal footprints).
* **Data Augmentation**: Heavy real-time image augmentation applied (Optical Zoom $\pm 20\%$, Shearing $\pm 20\%$, Horizontal Flipping, Rescaling to $[0, 1]$ range) to prevent model overfitting.
* **Network Layers**: 4-Stage Sequential CNN:
  * 3x Convolution Blocks (32, 32, and 64 filters using $1 \times 1$ kernels for channel-wise pooling + ReLU + MaxPool).
  * 1x Dense Layer (256 units + ReLU).
  * Ultra-aggressive regularization using `Dropout(0.8)` to counter medical dataset co-adaptation.
  * Final Softmax layer outputting categorical prediction probabilities.

### Model Evaluation Metrics
* **Accuracy**: **`93.4%`**
* **Precision**: **`92.1%`**
* **Recall (Sensitivity)**: **`94.6%`** *(High Recall ensures true positive diabetic neuropathic cases are not missed, which is vital for clinical safety)*
* **F1-Score**: **`93.3%`**

---

## 🛠️ Local Setup & Installation

Follow these steps to run the application locally on your Windows machine:

### Prerequisites
* Python 3.10 or 3.11 installed.
* Git installed.

### 1. Clone the Repository
```powershell
git clone https://github.com/dhruvdaberao/BE-Project.git
cd BE-Project
```

### 2. Set Up Virtual Environment & Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Modern Web Dashboard
```powershell
# Start the FastAPI server
python server.py
```
* Once the server starts, it will automatically open your default web browser to **`http://localhost:8000`**.
* The server will create the database `evaluation.db` and initialize the schema.

### 4. Run the Legacy Tkinter GUI (Optional)
If you wish to run the legacy offline desktop dashboard:
```powershell
python gui_main.py
```

---

## ☁️ Deployment (Render.com)

This app is optimized for seamless deployment to **Render.com** due to its low RAM footprint.

### Step-by-Step Instructions:
1. Log in to [Render.com](https://render.com) using your GitHub account.
2. Click **New +** > **Web Service**.
3. Link your `BE-Project` repository.
4. Apply the following settings:
   * **Runtime**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker server:app`
   * **Python Version**: Set `PYTHON_VERSION` environment variable to `3.10` or higher in **Advanced**.
5. Click **Create Web Service**. The deployment will complete, and Render will provide a public URL.

---

## 👥 Contributors

* **Dhruv Daberao** & Team
* Department of Computer Engineering
* Bachelor of Engineering (B.E.) Final Year Project

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
