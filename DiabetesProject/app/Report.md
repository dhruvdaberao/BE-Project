# Diabetes Tracker • Project Technical Report

## 1. Project Overview
The **Diabetes Tracker** is a professional-grade medical diagnostic platform designed to provide instantaneous diabetes risk assessments through clinical image analysis. Originally a legacy desktop application, it has been transformed into a modern, high-performance **Progressive Web App (PWA)** optimized for zero-latency cloud deployment.

## 2. Technology Stack
The application leverages a robust, industry-standard stack to ensure clinical reliability and user accessibility:

*   **Frontend**: Multi-platform Vanilla JS & CSS3 (Fully Responsive)
*   **Backend**: FastAPI (Python 3.10+) for high-concurrency request handling.
*   **Machine Learning**: TensorFlow & Keras (CNN models: `model1.h5`, `model2.h5`).
*   **Database**: SQLite (`evaluation.db`) for secure patient screening history.
*   **Deployment**: Render.com (Gunicorn + Uvicorn) for always-on accessibility.
*   **PWA**: Service Workers & Manifest integration for standalone mobile/desktop installation.

## 3. System Architecture
The project follows a decoupled **Client-Server Architecture**:
1.  **Client Layer**: A responsive dashboard that handles medical image uploads and state management.
2.  **Service Layer**: A RESTful API that coordinates authentication, history logging, and the ML pipeline.
3.  **Intelligence Layer**: A Deep Learning engine that preprocesses raw images and generates probabilistic risk scores.

## 4. Deep Learning Model (CNN)
The heart of the diagnostic engine is a **Convolutional Neural Network (CNN)** inspired by the AlexNet architecture.

### **Technical Specifics:**
*   **Input Dimensions**: 64 x 64 pixels.
*   **Data Type**: 3-channel RGB (Medical images are converted to RGB during the pipeline).
*   **Normalization**: Pixel values are normalized to a `[0, 1]` range for mathematical stability.
*   **Classes**: Supports multi-class classification (7 categories) which are aggregated into a binary "At Risk" or "Not At Risk" clinical report.

### **Data Flow Pipeline:**
1.  **Acquisition**: User uploads a standard clinical screening image.
2.  **Preprocessing**: Image is converted to Grayscale and Thresholded to highlight relevant vascular/tissue patterns.
3.  **Forward Pass**: The 64x64 normalized array is passed through multiple Convolutional and Pooling layers to extract features.
4.  **Inference**: The model outputs a probability score (Confidence Score), which is then mapped to a diagnostic label.

## 5. Challenges & Engineering Fixes

### **A. Git History Bloat (The 1GB Problem)**
*   **Challenge**: The repository became unusable when local virtual environments (`venv`) and massive TensorFlow DLLs (over 1007 MB) were accidentally tracked. This caused GitHub to reject and block all pushes.
*   **Fix**: Performed a **"Clean Slate" Reset**. I surgically purged the Git index, deleted the legacy history, and established a master `.gitignore` that definitively bans files over 100MB while keeping essential diagnostic models (`.h5`).

### **B. Deployment Path Constraints**
*   **Challenge**: Render.com rejected the original folder names (`100% Code.zip1`) because they contained illegal characters (percent signs and spaces).
*   **Fix**: Refactored the entire project directory to a clean `DiabetesProject/app` structure, ensuring full compatibility with cloud build systems.

### **C. User Interface Polish**
*   **Challenge**: Overlapping icons and clinical text created readability issues for health trends.
*   **Fix**: Injected high-priority **inline spacing (40px margins)** and defined a robust flex-gap utility system to ensure a premium, spacious UI/UX.

### **D. PWA Transformation**
*   **Challenge**: The app was tethered to a browser tab, making it feel less like a "medical tool."
*   **Fix**: Implemented a **Service Worker (sw.js)** and **Web App Manifest**. The platform is now "Installable" and appears as a native app on iOS, Android, and Windows.

## 6. Clinical Impact
By moving from a localized ZIP file to a cloud-hosted PWA, the Diabetes Tracker is now:
*   **Always-On**: Accessible by clinicians anywhere, anytime.
*   **Performant**: Uses high-performance inference to provide results in seconds.
*   **Actionable**: Includes a "Trend Analysis" system that calculates if a patient's health is improving or worsening based on their screening history.

---
**Report compiled by Dhruv Daberao.**
