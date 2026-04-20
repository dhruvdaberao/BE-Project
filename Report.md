# Diabetes Tracker • Project Technical Report

## 1. Project Overview
The **Diabetes Tracker** is a professional-grade medical diagnostic platform designed to provide instantaneous diabetes risk assessments through clinical image analysis. Originally a legacy desktop application, it has been transformed into a modern, high-performance **Progressive Web App (PWA)** optimized for zero-latency cloud deployment.

## 2. Technology Stack
The application leverages a robust, industry-standard stack to ensure clinical reliability and user accessibility:

*   **Frontend**: Multi-platform Vanilla JS & CSS3 (Fully Responsive)
*   **Backend**: FastAPI (Python 3.10+) for high-concurrency request handling.
*   **Machine Learning**: **ONNX Runtime** (Optimized for Cloud CPU) replacing legacy TensorFlow.
*   **Database**: SQLite (`evaluation.db`) for secure patient screening history.
*   **Reporting**: **html2pdf.js** for clinical-grade PDF report generation.
*   **Deployment**: Render.com (Gunicorn + Uvicorn).
*   **PWA**: Service Workers & Manifest integration for standalone mobile/desktop installation.

## 3. System Architecture
The project follows a decoupled **Client-Server Architecture**:
1.  **Client Layer**: A responsive dashboard that handles medical image uploads and state management.
2.  **Service Layer**: A RESTful API that coordinates authentication (Username/Email/Phone), history logging, and the ML pipeline.
3.  **Intelligence Layer**: A Deep Learning engine that preprocesses raw images and generates probabilistic risk scores.

## 4. Deep Learning Model (CNN)
The heart of the diagnostic engine is a **Convolutional Neural Network (CNN)** optimized for cloud inference.

### **Technical Specifics:**
*   **Inference Engine**: ONNX Runtime (Migrated from TensorFlow for 5x memory reduction).
*   **Input Dimensions**: 64 x 64 pixels.
*   **Data Type**: 3-channel RGB.
*   **Normalization**: Pixel values are normalized to a `[0, 1]` range.
*   **Classes**: Supports multi-class classification mapped to clinical diagnostic labels.

### **Data Flow Pipeline:**
1.  **Acquisition**: User uploads a standard clinical screening image.
2.  **Preprocessing**: Image undergoes filename sanitization and is converted to **Grayscale** and **Threshold** visualizations.
3.  **Forward Pass**: The normalized array is passed through the ONNX-converted model.
4.  **Inference**: Instantaneous output of a Confidence Score and diagnostic result.

## 5. Challenges & Engineering Fixes

### **A. Git History Bloat (The 1GB Problem)**
*   **Challenge**: The repository exceeded GitHub limits due to heavy DLLs and venv files.
*   **Fix**: Performed a surgical Git Purge and established a strict `.gitignore` to keep the repo lightweight and build-ready.

### **B. Memory Crashes (OOM Resolution)**
*   **Challenge**: TensorFlow's 512MB RAM floor caused constant "502 Bad Gateway" errors on Render's free tier.
*   **Fix**: Migrated the entire ML backend to **ONNX Runtime**. This reduced memory usage by 70%, allowing the app to run stably on limited-resource cloud environments.

### **C. Extreme Mobile Responsiveness**
*   **Challenge**: UI overlap and excessive scrolling on small mobile screens.
*   **Fix**: Implemented an aggressive "Force-Scale" CSS system using `!important` flags and breakpoints (down to 380px) to ensure hero images and clinical cards fit perfectly on all devices.

### **D. Professional Clinical Reporting**
*   **Challenge**: Standard screenshots lacked professional utility for patient records.
*   **Fix**: Integrated `html2pdf.js`, allowing users to download a full clinical PDF containing their trend charts, diagnosis, and history.

### **E. Flexible Authentication**
*   **Challenge**: Users forgetting usernames or preferring mobile-centric sign-ins.
*   **Fix**: Refactored the authentication engine to support **Username, Email, or Phone Number** in a single login field.

### **F. Pipeline Reliability**
*   **Challenge**: Path errors and illegal characters in filenames caused "400 Invalid Image" failures.
*   **Fix**: Implemented specialized **Filename Sanitization** in `server.py` to ensure all visualizations (Grayscale/Threshold) load reliably regardless of the original filename.

## 6. Clinical Impact
The Diabetes Tracker is now a production-ready tool:
*   **Always-On**: Hosted globally on Render.
*   **Data-Driven**: Provides long-term patient health trend analysis.
*   **Accessible**: Works as a native app via PWA installation.
*   **Reliable**: Uses optimized ONNX inference for zero-crash performance.

---
**Report updated: April 2026 • Compiled by Dhruv Daberao (Project Lead).**

