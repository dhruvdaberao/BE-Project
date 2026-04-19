# Diabetes Tracker • Deployment & Execution Guide

This document contains instructions for running the Diabetes Tracker locally on Windows and deploying the high-performance web dashboard to the cloud.

---

## 1. Local Execution (Windows)

Use these commands to run the application on your computer.

### A. Run Legacy GUI (Original Version)
If you wish to use the original Tkinter windowed application:
1. Open PowerShell or Command Prompt.
2. Run the following:
   ```powershell
   cd "c:\Users\dhruv\OneDrive\Desktop\SR_BE_Project\100% Code.zip1\100% Code"
   .\venv\Scripts\activate
   python "gui main.py"
   ```

### B. Run Modern Web Dashboard (Refined Version)
To run the new responsive web interface locally:
1. Open PowerShell.
2. Run the following:
   ```powershell
   cd "c:\Users\dhruv\OneDrive\Desktop\SR_BE_Project\100% Code.zip1\100% Code"
   .\venv\Scripts\activate
   python server.py
   ```
3. Open your browser to: **http://localhost:8000**

---

## 2. Cloud Deployment (Render.com)

To ensure the app **never sleeps** and stays **fast**, we recommend **Render.com**. It provides a robust, manageable environment for Python and Machine Learning.

### Step-by-Step Deployment:

1. **Prepare GitHub**:
   - Create a private repository on GitHub.
   - Upload all files from the `100% Code` folder to your GitHub repo.

2. **Connect to Render**:
   - Go to [Render.com](https://render.com/) and sign up with your GitHub account.
   - Click **"New +"** -> **"Web Service"**.
   - Connect the repository you just created.

3. **Configure Settings**:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 1 -k uvicorn.workers.UvicornWorker server:app`
   - **Plan Type**: 
     - *Free Tier*: App will sleep after 15 mins of inactivity.
     - *Individual/Starter ($7/mo)*: **Highly Recommended**. This keeps the app **Always-On** so analysis happens instantly without "waking up" the server.

4. **Environment Variables**:
   - Click the "Advanced" button.
   - Add a variable: `PYTHON_VERSION` = `3.10` (or higher).

5. **Deployment**:
   - Click **"Create Web Service"**.
   - Render will build the project and assign you a URL (e.g., `diabetes-tracker.onrender.com`).

---

## 3. Deployment Checklist

- [x] **Procfile**: Tells the server how to start the app.
- [x] **requirements.txt**: Lists all necessary medical and ML libraries.
- [x] **Static Files**: Navigation and UI assets are correctly located in `/static`.
- [x] **Performance**: Memory limit should be at least 2GB on the server to handle the Keras model smoothly.

> [!TIP]
> **Why Render over Vercel?**
> Vercel is built for simple websites and "sleeps" frequently. **Render** (on a Starter plan) is built for professional applications and keeps your Machine Learning model in memory. This eliminates the long "cold start" delay, making your analysis instantaneous for patients.
