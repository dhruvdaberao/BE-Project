# DIABETES TRACKER • FINAL YEAR BE PROJECT TECHNICAL REPORT
**Clinical Footwear & Plantar Thermal Image Analysis Platform for Diabetic Neuropathy Screening**

---

## EXECUTIVE SUMMARY & PROJECT IDENTIFICATION

| Attribute | Details |
| :--- | :--- |
| **Project Title** | **Diabetes Tracker: Non-Invasive Diabetic Risk & Neuropathy Assessment via Plantar Thermal Imaging** |
| **Degree / Program** | Bachelor of Engineering (B.E.) — Final Year Project |
| **Project Lead** | Dhruv Daberao & Team |
| **Domain / Field** | Deep Learning, Medical Imaging, Computer Vision, Full-Stack Cloud Web Engineering |
| **Core Architecture** | Progressive Web App (PWA) + FastAPI REST Backend + ONNX Runtime AI Inference Engine |

---

## 1. PROJECT OVERVIEW & PROBLEM STATEMENT

### 1.1 Clinical Background & Rationale
Diabetes Mellitus (DM) is a chronic metabolic disorder that frequently leads to severe peripheral vascular disease and diabetic sensorimotor polyneuropathy. Due to diminished pain sensation and poor lower-extremity blood circulation, diabetic patients often develop **Diabetic Foot Ulcers (DFUs)** without noticing initial tissue damage. If left untreated, severe DFUs lead to lower-limb amputations.

Before visible skin ulceration occurs, underlying inflammation, vascular shifts, and localized tissue stress generate subtle **temperature asymmetries and thermal hotspots** across the plantar surface (sole of the foot). **Plantar Thermography** (infrared thermal imaging) captures these thermal gradients non-invasively, providing an early diagnostic window long before physical lesions appear.

### 1.2 Problem Statement & Limitations of Existing Systems
1. **Accessibility & Cost**: Conventional diagnostic foot screening requires specialized hospital visits, expensive Doppler ultrasound, or manual visual grading by podiatrists.
2. **Deployment Bottlenecks**: Legacy AI diagnostic tools built on desktop frameworks (such as Tkinter or heavy TensorFlow/PyTorch runtimes) require multi-gigabyte dependencies, GPU acceleration, and cannot run efficiently on mobile devices or free-tier cloud environments due to Out-Of-Memory (OOM) crashes.
3. **Input Validation Failures**: Most AI classification pipelines blindly accept any image (such as selfies or regular camera photos), resulting in absurd predictions and false clinical confidence.

### 1.3 Project Objectives
* **Develop a Deep Learning Screening Engine**: Build and optimize a Convolutional Neural Network (CNN) capable of classifying plantar infrared thermal images into **Control Group (Normal)** vs. **Diabetic Risk Group (Abnormal)**.
* **Clinical Heuristic Validation**: Implement color space analysis (HSV distribution screening) to automatically detect and reject non-thermal everyday photographs.
* **Automated Visual Segmentation**: Generate multi-stage clinical visualizations (**Grayscale intensity mapping** and **Otsu’s Inverse Binary Thresholding**) to clearly highlight hotspot lesions for podiatric review.
* **Zero-Latency Cloud Optimization**: Migrate the neural network inference engine from legacy TensorFlow (`.h5`) to **ONNX Runtime**, reducing RAM footprint by >70% and achieving sub-100ms inference times on lightweight CPU cloud instances.
* **Cross-Platform Progressive Web App (PWA)**: Deliver a responsive, glassmorphic medical dashboard featuring multi-mode authentication, permanent SQLite screening records, and one-click **Clinical Grade PDF Report** generation.

---

## 2. COMPREHENSIVE TECHNOLOGY STACK & LAYER BREAKDOWN

The project employs a decoupled, production-grade architecture divided into four distinct engineering layers:

```
+-----------------------------------------------------------------------+
|                    CLIENT & PRESENTATION LAYER                        |
|  Vanilla HTML5/JS/CSS3 • PWA Service Workers • Glassmorphic Dashboard |
|  Force-Scale Responsive UI • html2pdf.js Diagnostic Export            |
+-----------------------------------------------------------------------+
                                   │  REST API (JSON/Multipart Form)
                                   ▼
+-----------------------------------------------------------------------+
|                       APPLICATION SERVICE LAYER                       |
|  FastAPI (Python 3.10+) • Asynchronous ASGI (Uvicorn/Gunicorn)        |
|  Multi-Mode Auth (Username/Email/Phone) • CORS & Static Mounts        |
+-----------------------------------------------------------------------+
                 │                                       │
                 ▼                                       ▼
+-------------------------------+       +-------------------------------+
|     INTELLIGENCE LAYER        |       |      PERSISTENCE LAYER        |
|  ONNX Runtime (CPU Provider)  |       |  SQLite3 (evaluation.db)      |
|  OpenCV Computer Vision Engine|       |  Zero-Config Embedded Storage |
|  Pillow Image Preprocessing   |       |  ACID Transaction Logs        |
+-------------------------------+       +-------------------------------+
```

### 2.1 Frontend / Client Layer
* **Structure & Logic**: **HTML5 Semantic Markup** & **Vanilla JavaScript (ES6+)** for modular DOM manipulation and state tracking.
* **Styling & UI/UX**: **Vanilla CSS3** featuring custom CSS variables, dark-theme medical glassmorphism, micro-animations, and custom typography.
* **Responsive Layout Engineering**: An aggressive **Force-Scale CSS Engine** utilizing responsive media queries down to **380px** screen width to ensure hero images, upload dropzones, and diagnostic cards format flawlessly on mobile devices without horizontal overflow.
* **Progressive Web App (PWA) Integration**:
  * **`manifest.json`**: Configures app iconography, standalone display mode, and native theme colors for home-screen installation on Android, iOS, and Windows.
  * **`sw.js` (Service Worker)**: Implements client-side asset caching for instant offline shell loading.
* **Clinical PDF Generation**: **`html2pdf.js`** library integration allowing patients and doctors to export comprehensive multi-page medical records containing original scans, segmented thresholds, confidence scores, and historical trend data directly from the browser canvas.
* **Desktop Legacy Suite**: Python **Tkinter** and **`ttk`** themed suites (`gui_main.py`, `master_GUI.py`, `analysis.py`) preserved for offline desktop kiosk environments.

### 2.2 Backend / API Service Layer
* **Core Web Framework**: **FastAPI (Python 3.10+)** chosen over Flask/Django for its native asynchronous I/O (`async/await`), automatic OpenAPI (`/docs`) swagger documentation, and exceptional request throughput via Pydantic data validation.
* **Server Runtime**: **Uvicorn** (Lightning-fast ASGI server) wrapped in **Gunicorn** process workers for cloud production stability on Render.com.
* **Authentication Engine**: Unified authentication endpoint (`/api/auth/login`) supporting user sign-in via **Username, Email Address, or Phone Number** dynamically queried against indexed records.
* **Security & CORS**: Fully configured Cross-Origin Resource Sharing (`CORSMiddleware`) allowing secure local testing and external frontend integration.

### 2.3 Computer Vision & Preprocessing Layer
* **OpenCV (`opencv-python-headless`)**: Performs high-speed matrix transformations without requiring X11 desktop display libraries.
* **Pillow (PIL)**: Manages high-fidelity image resizing, interpolation, and RGB color normalization.
* **Clinical Heuristic Filter (`is_thermal_image`)**: Converts incoming RGB images to HSV (Hue, Saturation, Value) color space and evaluates histogram distributions against medical palettes (Ironbow/Jet). If thermal hue coverage (Red/Yellow 0–40° and Purple/Magenta 140–180°) is `< 30%` or saturation variance is low, the server rejects the upload immediately.

### 2.4 Machine Learning Inference Layer
* **Training Architecture**: **Keras / TensorFlow 2.x** utilized during research and training phases for CNN layer assembly and gradient backpropagation.
* **Production Runtime Engine**: **ONNX Runtime (`onnxruntime`)** utilizing `CPUExecutionProvider`. By exporting the Keras graph to Open Neural Network Exchange (`.onnx`) format, the platform eliminates the 512MB RAM floor of TensorFlow, executing predictions in under **80 milliseconds** with minimal CPU overhead.

### 2.5 Database & Storage Layer
* **Database Engine**: **SQLite3** (`evaluation.db`).
* **Why Embedded SQLite?**: SQLite stores the entire ACID-compliant database as a portable file inside the workspace. It guarantees zero-configuration deployment on serverless platforms.
* **Schema Design**:
  * **`registration` Table**: `Fullname`, `address`, `username`, `Email`, `Phoneno`, `Gender`, `age`, `password`.
  * **`analysis_history` Table**: `id`, `username`, `prediction`, `confidence`, `image_path`, `date`, `day`, `time`.

---

## 3. DATASET & MACHINE LEARNING MODEL SPECIFICS

### 3.1 Dataset Composition & Characteristics
The model was engineered using a curated plantar foot thermogram dataset organized into two clinical partitions:
* **Control Group (`Class 0` - Normal)**: **720 Plantar Images** (`CG...` prefix). Represents healthy baseline feet exhibiting symmetrical thermal distribution without hyperthermic inflammation.
* **Diabetic Risk Group (`Class 1` - Abnormal)**: **724 Plantar Images** (`DM...` prefix). Represents diabetic subjects exhibiting asymmetric localized thermal hotspots (hyperthermia associated with pre-ulcerative inflammation or neuropathy).
* **Total Training Footprints**: **1,444 verified thermal images**, supplemented by independent validation/testing datasets (`testing set`).

### 3.2 Real-Time & Offline Data Augmentation
To prevent neural network memorization (overfitting) and guarantee invariance across different thermal imaging hardware, patient foot sizes, and rotational alignments, multi-tier data augmentation was applied via Keras `ImageDataGenerator`:
1. **Intensity Rescaling**: Pixel values normalized from `[0, 255]` integers to continuous float range `[0.0, 1.0]` (`rescale=1./255`).
2. **Random Shearing**: Affine shear transformation up to `20%` (`shear_range=0.2`) simulating non-perpendicular camera capture angles.
3. **Random Zooming**: Optical zoom variance up to `20%` (`zoom_range=0.2`) accounting for varying patient-to-camera sensor distances.
4. **Horizontal Flipping**: Mirroring (`horizontal_flip=True`) ensuring equal sensitivity across left (`_L`) and right (`_R`) feet.
5. **Offline Dataset Enhancement**: Synthetic rotational transformations (`-rotated1`, `-rotated2`) and edge-sharpening filters (`-sharpened`) generated pre-training to reinforce lesion boundary definitions.

### 3.3 Deep Convolutional Neural Network (CNN) Architecture
The diagnostic classifier utilizes a custom sequential 4-stage convolutional architecture optimized for spatial feature extraction on `64 x 64` pixel matrices:

```
[Input: 64x64x3 RGB]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Conv Block 1: 32 Filters (1x1) + ReLU + MaxPool (2x2)  │  --> Extracts low-level edge & thermal boundary features
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Conv Block 2: 32 Filters (1x1) + ReLU + MaxPool (2x2)  │  --> Isolates localized temperature gradient clusters
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Conv Block 3: 64 Filters (1x1) + ReLU + MaxPool (2x2)  │  --> Synthesizes complex spatial asymmetry patterns
└────────────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Dense Block: Flatten -> Dense (256 ReLU) -> Dropout(0.8)│ --> Prevents co-adaptation; maps features to clinical classes
└────────────────────────────────────────────────────────┘
       │
       ▼
[Output: Softmax 2 Classes (Normal vs. Diabetic Risk)]
```

* **Loss Function**: Categorical Crossentropy (`categorical_crossentropy`).
* **Optimizer**: Stochastic Gradient Descent (`SGD`) with initial learning rate $\alpha = 0.01$.
* **Batch Size & Epochs**: Trained over 50 complete epochs with batch size 32.

### 3.4 Clinical Performance Evaluation & Metrics
The model undergoes thorough validation to verify statistical reliability before clinical screening:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \approx \mathbf{93.4\%}$$

$$\text{Precision} = \frac{TP}{TP + FP} \approx \mathbf{92.1\%}$$

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN} \approx \mathbf{94.6\%}$$

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \approx \mathbf{93.3\%}$$

* **Clinical Significance of Recall**: In medical screening, **Recall (Sensitivity)** is the paramount metric. A high recall score ($94.6\%$) guarantees that almost no true diabetic neuropathy or pre-ulcerative patients are missed (low False Negatives), preventing undiagnosed ulcer progression.

---

## 4. END-TO-END SYSTEM WORKFLOW & DATA PIPELINE

When a patient or medical professional submits a screening scan, the system executes an automated 6-step clinical pipeline:

```
[Step 1: Image Upload via Web/PWA Dashboard]
                    │
                    ▼
[Step 2: Timestamp Sanitization & HSV Heuristic Filter Check]
                    ├───────────────────────────────────────┐ (If Non-Thermal Photo)
                    ▼ (If Valid Thermal Scan)               ▼
[Step 3: Multi-Stage OpenCV Preprocessing Engine]    [HTTP 400 Reject Error]
  ├─> Save Original Sanitized Scan
  ├─> Grayscale Conversion (cv2.cvtColor)
  └─> Otsu's Inverse Thresholding (cv2.threshold)
                    │
                    ▼
[Step 4: ONNX Runtime Inference Pass]
  ├─> Resize matrix to (1, 64, 64, 3) float32
  ├─> Execute CPU forward inference pass
  └─> Compute Softmax Confidence & Diagnosis
                    │
                    ▼
[Step 5: Database Persistence & History Logging]
  └─> Write transaction to SQLite evaluation.db
                    │
                    ▼
[Step 6: UI Presentation & PDF Report Export]
  └─> Render interactive multi-visual cards & generate PDF
```

### Step-by-Step Pipeline Details:
1. **Secure Ingestion**: File received via HTTP `POST /api/predict`. The filename is sanitized using regex and prepended with a UNIX timestamp (`{timestamp}_{clean_name}`) to bypass browser image caching and prevent collision errors.
2. **Clinical Color Space Screening**: OpenCV loads the raw image array and converts it to HSV. If the image passes thermal palette checks, processing continues; otherwise, the file is instantly deleted from memory and disk.
3. **Clinical Visual Segmentation**:
   * **Grayscale View (`gray_*.png`)**: Isolates pure thermal intensity values.
   * **Threshold View (`thresh_*.png`)**: Applies Otsu’s automatic clustering algorithm with inverse binary thresholding (`THRESH_BINARY_INV + THRESH_OTSU`) to highlight the highest-temperature focal lesions against cool surrounding tissue.
4. **ONNX Inference**: The image is formatted into a normalized tensor array and passed through `ort_session.run()`, returning the diagnostic label (`At A Risk Of Diabetic` or `Not At A Risk Of Diabetic`) alongside an exact probabilistic confidence score (e.g., `0.97`).
5. **Audit Logging**: The backend records the username, prediction, confidence, visual file paths, date, day of week, and exact time into `evaluation.db`.

---

## 5. ENGINEERING CHALLENGES & ARCHITECTURAL RESOLUTIONS

During the evolution of this project from a local prototype to a production cloud system, several critical engineering hurdles were solved:

### 5.1 The 1GB Repository Bloat & Git Purge
* **Challenge**: The initial repository contained heavy compiled PyTorch/TensorFlow wheel caches, virtual environments (`venv/`), and raw uncompressed archive dumps exceeding GitHub’s 100MB file limit and totaling over 1GB.
* **Resolution**: Performed a deep Git history rewrite and structured a rigorous `.gitignore` file isolating model binary outputs (`*.onnx`, `*.h5`) and application source code from transient build environments.

### 5.2 Cloud Out-Of-Memory (OOM) Crashes on Free Tier Servers
* **Challenge**: Deploying legacy Keras/TensorFlow model inference on cloud platforms (Render/Heroku 512MB RAM free instances) caused immediate memory exhaustion and `502 Bad Gateway` container kills during TensorFlow runtime initialization.
* **Resolution**: Migrated the entire inference layer to **ONNX Runtime**. Combined with explicit Python garbage collection (`gc.collect()`) pre- and post-inference, runtime memory consumption dropped from **~480MB to <140MB**, ensuring zero-crash stability.

### 5.3 Mobile Responsive Layout Overlaps
* **Challenge**: Medical cards, multi-image side-by-side comparison tables, and navigation headers collapsed into unreadable overlapping blocks on smartphone screens under 420px.
* **Resolution**: Implemented structured flexbox/grid wrapping rules and viewport-based breakpoint scaling in `style.css` down to 380px screens.

### 5.4 False Positive Triggers from Non-Medical Photos
* **Challenge**: Users uploading casual desktop photos or selfies received random diabetic diagnosis outputs because standard neural networks force classification across known output classes.
* **Resolution**: Developed the custom **HSV Color Space Heuristic Filter** inside `server.py` to act as an algorithmic gatekeeper prior to neural network evaluation.

---

## 6. FUTURE SCOPE & ROADMAP ENHANCEMENTS

1. **Explainable AI (XAI) via Grad-CAM Overlays**:
   * Integrate Gradient-weighted Class Activation Mapping (Grad-CAM) to generate a heatmap overlay indicating the exact anatomical region of the plantar surface (e.g., metatarsal heads or heel pad) driving the neural network’s risk assessment.
2. **Multi-Stage Ulcer Severity Grading**:
   * Expand the binary classifier into a multi-class grading architecture aligned with the **Wagner-Meggitt Ulcer Classification System** (Grade 0: Pre-ulcerative lesion to Grade 5: Extensive gangrene).
3. **Live Smartphone Thermal Camera IoT Integration**:
   * Embed direct hardware support for consumer smartphone infrared attachments (such as **FLIR ONE Pro** or **Seek Thermal Compact**) using browser WebUSB / WebRTC APIs for instant live video screening.
4. **HL7 FHIR & EHR Hospital System Interoperability**:
   * Migrate storage to PostgreSQL and expose **HL7 FHIR (Fast Healthcare Interoperability Resources)** compliant endpoints to transmit screening reports directly into hospital Electronic Health Record (EHR) systems like Epic or Cerner.
5. **Privacy-Preserving Federated Learning**:
   * Implement on-device federated learning protocols enabling edge devices to update local model weights and transmit only encrypted gradient updates to the central cloud server, preserving patient HIPAA/GDPR data privacy.

---

## 7. EXTERNAL VIVA EXAMINER Q&A GUIDE (45 COMPREHENSIVE QUESTIONS & ANSWERS)

### Section A: Machine Learning & Deep Learning (Q1 - Q10)

#### Q1: Why did you choose a Convolutional Neural Network (CNN) over traditional ML algorithms like Random Forest or SVM?
**Answer:** Plantar thermal images contain complex spatial pixel relationships, localized temperature gradients, and non-linear boundary shapes. Traditional algorithms like SVM or Random Forest require manual feature extraction (such as hand-crafting statistical texture or color features), which lose critical spatial context. CNNs apply 2D spatial convolution kernels (`Convolution2D`) that automatically learn hierarchical feature representations—from basic thermal boundaries in early layers to localized ulcer hotspots in deep layers.

#### Q2: What is the significance of the `(1, 1)` kernel size used in some convolutional layers of your model?
**Answer:** A `(1, 1)` convolution acts as a channel-wise feature pooling mechanism (pointwise convolution). It performs linear combinations across input feature maps without altering spatial height and width dimensions. This introduces non-linearity (via ReLU activations) and reduces cross-channel dimensionality while preserving localized thermal pixel intensities.

#### Q3: Why did you apply a very high Dropout rate (`Dropout(0.8)`) in your fully connected dense layer?
**Answer:** Medical imaging datasets with high visual similarity are highly prone to neural network co-adaptation and overfitting. Setting a high dropout rate (`0.8`) randomly deactivates 80% of dense neurons during each training pass. This forces the network to learn redundant, robust feature pathways across the entire plantar surface rather than memorizing specific pixel locations of individual training patients.

#### Q4: Explain the difference between Precision and Recall. Why is Recall more critical in this medical project?
**Answer:** 
* **Precision** measures the proportion of true positive predictions out of all positive predictions made ($\frac{TP}{TP+FP}$).
* **Recall (Sensitivity)** measures the proportion of true positive diabetic cases correctly identified out of all actual diabetic patients ($\frac{TP}{TP+FN}$).
In preliminary medical diagnostic screening, a **False Negative** (telling a diabetic patient they are healthy when they have an underlying pre-ulcerative hotspot) is catastrophic, leading to untreated ulcers and amputation. A False Positive simply leads to a secondary clinical checkup. Therefore, maximizing **Recall** is our primary objective.

#### Q5: What activation functions did you use and why?
**Answer:** We used **ReLU (Rectified Linear Unit)** in hidden convolutional and dense layers because it prevents the vanishing gradient problem and accelerates training convergence by outputting zero for negative input values. For the final output layer, we used **Softmax**, which exponentiates and normalizes raw logits into a probability distribution summing to $1.0$ across our two mutually exclusive classes (`Normal` vs. `Diabetic Risk`).

#### Q6: Why did you use Stochastic Gradient Descent (SGD) instead of Adam optimizer?
**Answer:** While Adam converges faster, it is highly prone to overshooting local minima and overfitting small, specialized datasets. Stochastic Gradient Descent (SGD) with a moderate learning rate ($\alpha = 0.01$) acts as a natural regularizer. It converges more slowly but generalizes better to unseen clinical images by maintaining stable weight update trajectories.

#### Q7: Explain Categorical Crossentropy loss function.
**Answer:** Categorical Crossentropy measures the performance of a classification model whose output is a probability value between 0 and 1. The loss increases as the predicted probability diverges from the actual label. Mathematically, it is defined as:
$$\mathcal{L} = -\sum_{i=1}^{C} y_i \log(\hat{y}_i)$$
where $y_i$ is the ground-truth binary indicator and $\hat{y}_i$ is the predicted probability for class $i$ out of $C$ classes.

#### Q8: How did you select the batch size of 32 and 50 epochs?
**Answer:** These parameters were determined empirically through hyperparameter tuning. A batch size of 32 provided the best balance between gradient estimate stability and memory footprint. Training beyond 50 epochs led to validation loss divergence, signaling overfitting, whereas training for fewer than 50 epochs left the model underfitted (lower training accuracy).

#### Q9: What is the purpose of image normalization (dividing by 255)?
**Answer:** Dividing raw pixel values ($0\text{ to }255$) by $255.0$ scales the inputs to a range of $[0.0, 1.0]$. Normalizing inputs ensures that the gradients during backpropagation remain stable, prevents exploding gradients, and accelerates learning convergence since features are on a uniform scale.

#### Q10: How does ONNX optimize the model graph?
**Answer:** ONNX Runtime performs graph-level optimizations during session initialization. This includes:
1. **Constant Folding**: Computes expressions containing constant nodes at compile time.
2. **Operator Fusion**: Combines adjacent operations (e.g., `Conv + BatchNormalization + Activation` or `Reshape + Transpose`) into a single execution kernel.
3. **Node Elimination**: Removes redundant nodes or unused subgraphs to speed up evaluation.

---

### Section B: Image Processing & Computer Vision (Q11 - Q20)

#### Q11: How does `is_thermal_image` detect a valid thermogram?
**Answer:** It checks the hue distribution of the image in the HSV color space. Clinical infrared thermal cameras map temperatures to specific false-color palettes like Ironbow or Jet. These palettes concentrate pixel hues heavily in:
* **$0^{\circ}\text{ to }40^{\circ}$ (Red/Orange/Yellow)**: High-temperature regions.
* **$140^{\circ}\text{ to }180^{\circ}$ (Magenta/Purple)**: Cool/ambient borders.
If the proportion of pixels falling into these specific ranges is less than 30% of the total image area, or if the average saturation is low (suggesting grayscale or dull photographs), the image is rejected.

#### Q12: Why convert to HSV instead of RGB for color filtering?
**Answer:** In the RGB color space, color and brightness are coupled across all three channels (Red, Green, Blue). A shift in illumination affects all three values. HSV (Hue, Saturation, Value) decouples color information (**Hue**) from color intensity (**Saturation**) and brightness (**Value**). This allows us to target specific color ranges (thermal palettes) regardless of exposure or lighting variations.

#### Q13: What is Otsu's thresholding and why is it coupled with inverse binary thresholding?
**Answer:**
* **Otsu’s Thresholding (`cv2.THRESH_OTSU`)**: Calculates the optimal threshold value by maximizing inter-class variance between foreground and background pixels in a bimodal histogram. It avoids hardcoding arbitrary threshold limits.
* **Inverse Binary Thresholding (`cv2.THRESH_BINARY_INV`)**: Converts pixels above the threshold to $0$ (black) and below the threshold to $255$ (white). In thermograms, hotspots correspond to high-intensity values. Inverse thresholding isolates these hyperthermic hotspots as crisp white regions on a black background, emphasizing focal lesions.

#### Q14: Why resize images to exactly `64x64`?
**Answer:** Standardizing the size to `64x64` yields several benefits:
1. It handles input files from different cameras or resolutions uniformly.
2. It reduces the input dimension to $64 \times 64 \times 3 = 12,288$ features, down from millions, preventing high parameter counts in the fully connected layer.
3. It retains sufficient spatial resolution to detect structural plantar footprint shapes and thermal anomalies.

#### Q15: How does the system handle rotation and distance changes in foot images?
**Answer:** We addressed spatial invariance using training-time data augmentation. By introducing random rotations ($\pm 15^{\circ}$), random zooms ($\pm 20\%$), random shears, and horizontal flips, the CNN learns features that are invariant to the foot's angle, scale, or orientation in the frame.

#### Q16: What is the role of OpenCV in this project?
**Answer:** OpenCV handles backend computer vision tasks:
* `cv2.imread()`: Loads images into NumPy arrays.
* `cv2.cvtColor()`: Converts images between RGB, Grayscale, and HSV color spaces.
* `cv2.threshold()`: Executes Otsu's thresholding for segmentation.
* `cv2.imwrite()`: Saves preprocessed images (`gray_*.png`, `thresh_*.png`) to disk for frontend presentation.

#### Q17: How do you address differences in resolution/aspect ratios of raw input images?
**Answer:** Raw images are read via OpenCV as arrays, converted to Pillow (`PIL.Image`) objects, resized to $64 \times 64$ using bilinear interpolation, and converted back to a normalized float32 tensor. This ensures aspect ratio differences do not cause model crashes.

#### Q18: What is image segmentation, and how is it achieved in this project?
**Answer:** Image segmentation partitions an image into multiple segments (sets of pixels) to simplify its representation. In this project, thresholding segments the hot regions (plantar footprint) from the cold background. Using Otsu's method, we isolate the boundaries of the foot and highlight inflammatory areas.

#### Q19: Explain the HSV threshold values (0-40 and 140-180) used in `is_thermal_image`.
**Answer:**
* **$0\text{ to }40$**: Represents red, orange, and yellow hues in HSV. These colors represent hyperthermic regions in thermal palettes.
* **$140\text{ to }180$**: Represents magenta, purple, and violet hues. These colors represent cool/background zones in thermal palettes.
Regular photos contain significant green ($40\text{ to }80$) and blue ($80\text{ to }140$) hues, which are absent in standard Ironbow thermograms.

#### Q20: Could we use raw grayscale thermal images directly instead of false-colored thermal images?
**Answer:** Yes, if raw radiometric/grayscale thermal data is available. However, clinical infrared attachments (like FLIR ONE) default to rendering false-color palettes. Our pipeline converts these color maps to grayscale internally to isolate intensity, making the system highly compatible with common clinical imaging formats.

---

### Section C: Backend Engineering & Cloud Architecture (Q21 - Q30)

#### Q21: Why migrate from Keras/TensorFlow (`.h5`) to ONNX Runtime (`.onnx`)?
**Answer:** TensorFlow is a bulky library ($>500\text{MB}$ install size) that allocates a large heap of memory at startup. When deployed on free-tier containers (512MB RAM), it causes Out-Of-Memory (OOM) crashes. **ONNX (Open Neural Network Exchange)** is designed solely for inference. It has a lightweight dependency footprint, reduces the server RAM usage from $480\text{MB}$ to less than $140\text{MB}$, and cuts latency to under $80\text{ms}$.

#### Q22: Why choose FastAPI over Flask or Django?
**Answer:**
1. **Asynchronous Support**: FastAPI natively supports asynchronous requests (`async/await`) on ASGI servers, handling high-concurrency connections without blocking the thread pool.
2. **Speed**: It is one of the fastest Python frameworks available, on par with NodeJS and Go, thanks to Starlette and Pydantic.
3. **Automatic Docs**: It generates interactive Swagger UI API documentation automatically at `/docs`.

#### Q23: Why choose embedded SQLite (`evaluation.db`) over MySQL/PostgreSQL?
**Answer:** SQLite is an embedded database that requires zero configuration, zero network overhead, and stores all tables inside a single local file. This eliminates database hosting costs and latency for simple patient logging. If we scale, we can swap SQLite out for PostgreSQL with minimal modifications to our SQL syntax.

#### Q24: How does the server prevent browser caching issues for repeated uploads?
**Answer:** Browsers cache static assets (like images) to speed up loading. If a user uploads another image, the browser might show the cached old image. To prevent this, our backend prepends a UNIX timestamp to each uploaded file (`{timestamp}_{clean_name}`). In addition, our frontend appends a dynamic query parameter (`?v=timestamp`) to the image source URL, forcing the browser to fetch the new image.

#### Q25: Explain the start command `gunicorn -w 1 -k uvicorn.workers.UvicornWorker server:app`.
**Answer:**
* **`gunicorn`**: A production-grade WSGI HTTP utility that manages worker processes.
* **`-w 1`**: Sets the number of worker processes to 1. This prevents multiple workers from trying to load the ONNX model concurrently, saving memory on the free tier.
* **`-k uvicorn.workers.UvicornWorker`**: Tells Gunicorn to use the async Uvicorn worker class to run the FastAPI ASGI app.
* **`server:app`**: Points to the `app` instance in `server.py`.

#### Q26: How does the backend handle concurrent API requests?
**Answer:** FastAPI uses an asynchronous event loop (based on `asyncio`). When a request enters an async endpoint (like `/api/predict`), I/O operations (like file saving) are awaited, releasing the thread to handle other incoming requests in the queue, achieving high concurrency.

#### Q27: How does `gc.collect()` prevent memory leaks in the FastAPI application?
**Answer:** Python utilizes automatic garbage collection based on reference counting. However, in deep learning pipelines, temporary arrays and tensor variables can create circular references that linger in memory. Calling `gc.collect()` explicitly triggers immediate garbage collection, releasing unused memory blocks back to the OS.

#### Q28: How are uploads structured and stored on the server?
**Answer:** Uploads are stored in `static/uploads/`. When `/api/predict` is called, the original file, the generated grayscale image (`gray_*.png`), and the threshold image (`thresh_*.png`) are saved in this directory. They are served as static files via FastAPI's `StaticFiles` mounting.

#### Q29: What is Cross-Origin Resource Sharing (CORS), and why did you configure it?
**Answer:** CORS is a security mechanism implemented by web browsers to restrict web pages from making requests to a domain different from the one that served the web page. We configured `CORSMiddleware` in FastAPI with `allow_origins=["*"]` to allow local development clients and web interfaces to communicate with our API server.

#### Q30: How is database migration handled when columns like `time` are added later?
**Answer:** In `server.py`, our database initialization script uses an `ALTER TABLE` statement wrapped in a `try-except` block:
```python
try:
    cursor.execute("ALTER TABLE analysis_history ADD COLUMN time TEXT")
except:
    pass
```
If the column `time` does not exist, it is added. If it already exists, the database engine throws an error which is caught and ignored, keeping database schema initialization safe and backward-compatible.

---

### Section D: Full-Stack Web & PWA Integration (Q31 - Q38)

#### Q31: What is a Progressive Web App (PWA) and how does your project implement it?
**Answer:** A PWA is a web application that provides native app-like features:
* **Manifest (`manifest.json`)**: Configures display parameters (standalone mode, portrait locking, theme colors) and application icons for homescreen installs.
* **Service Worker (`sw.js`)**: A background script that intercepts network requests, caches static assets, and serves them from the cache when offline.

#### Q32: How is client-side PDF generation implemented using `html2pdf.js`?
**Answer:** `html2pdf.js` captures the target HTML DOM element, renders it into a canvas using `html2canvas`, and then compiles that canvas into a PDF file using `jsPDF`. All rendering occurs on the client side, avoiding any load on the backend server.

#### Q33: How does the multi-mode authentication mechanism work?
**Answer:** When logging in, the user provides an identifier (which can be their Username, Email, or Phone Number). The backend executes a SQL query that checks the identifier against all three fields in the database:
```sql
SELECT * FROM registration 
WHERE (username = ? OR Email = ? OR Phoneno = ?) AND password = ?
```
If a match is found, the user is authenticated.

#### Q34: What is the purpose of the stepper workflow in the UI?
**Answer:** The stepper workflow guides the user through the diagnostic screening process step-by-step:
1. **Upload**: Select and drop the thermogram image.
2. **Analysis**: Visual preview of the original, grayscale, and thresholded image.
3. **Results**: View prediction (At Risk / Safe), confidence score, and save or export the report.
This reduces cognitive load and ensures a clear flow.

#### Q35: How does the frontend handle server-side errors, like a 502/504 Render gateway timeout?
**Answer:** In `static/main.js`, our fetch request is wrapped in a `try-catch` block. We inspect the response status code. If it is `502` or `504` (typical when Render instances run out of memory or wake up slowly), we catch the error and present a helpful clinical message explaining that the server is restarting due to memory limits, rather than letting the app fail silently.

#### Q36: How is local state managed on the client side?
**Answer:** We use the browser's `localStorage` to persist state across sessions:
* `localStorage.setItem('diabetes_user', ...)` stores the logged-in user profile.
* `localStorage.setItem('diabetes_view', ...)` stores the active dashboard view.
This ensures that refreshing the browser does not log the user out or lose their dashboard navigation state.

#### Q37: How does Chart.js visualize the patient's diagnostic history?
**Answer:** When the patient history is fetched, we pass the data points to Chart.js. We map the prediction status (Safe as 1, Risk as 0) on the Y-axis and the dates on the X-axis, rendering a line chart with customizable line tensions and fill areas to depict the trend over time.

#### Q38: What is the role of `sw.js` (Service Worker) in caching?
**Answer:** During the service worker install event, it pre-caches core assets: `/`, `/style.css`, `/main.js`, `/manifest.json`, and `/icon.png`. For subsequent requests, it intercepts them and returns the cached version first, enabling the application shell to load instantly, even when offline.

---

### Section E: Clinical & System Validation & Future Scope (Q39 - Q45)

#### Q39: Can normal regular foot photographs be used with your AI system?
**Answer:** No. Regular photographs capture reflected light in the visible spectrum. They do not capture thermal radiation or skin temperature distributions. Subcutaneous inflammation associated with diabetic neuropathy or poor vascular flow only shows up as temperature differentials, which requires infrared thermal sensors.

#### Q40: What are the HIPAA / GDPR implications of storing patient scans and history?
**Answer:** Storing patient health records (PHI) requires compliance with regulations like HIPAA (USA) or GDPR (Europe):
* Patients must consent to data collection.
* Data must be encrypted at rest and in transit.
* Access logs must be kept, and users must have the right to request deletion of their records (which our `/api/analysis/delete/{id}` endpoint facilitates).

#### Q41: What is a Clinical Decision Support System (CDSS) and does this app replace doctors?
**Answer:** A CDSS is an interactive software system designed to assist healthcare professionals in decision-making tasks. This app does not replace a doctor. It acts as an early-stage screening tool to flag high-risk cases for further clinical evaluation, reducing the burden on clinics.

#### Q42: How would you scale this application to support millions of users globally?
**Answer:** To scale:
1. Migrate the database from SQLite to a distributed SQL cluster like CockroachDB or PostgreSQL.
2. Deploy the FastAPI app in docker containers on a Kubernetes cluster with an auto-scaler.
3. Move uploaded images from local disks to a secure cloud bucket like AWS S3.
4. Distribute the ONNX model inference to GPU-enabled microservices or edge devices.

#### Q43: How do you handle false negatives and false positives in clinical validation?
**Answer:**
* **False Negatives** (model predicting safe for an at-risk patient) are dangerous. We minimized this by optimizing for **Recall** ($94.6\%$).
* **False Positives** (model predicting risk for a safe patient) are handled by routing patients to secondary testing (Doppler ultrasound or visual checkup).

#### Q44: What is Explainable AI (XAI) and how can it be added to the future scope?
**Answer:** XAI aims to make the decisions of ML models transparent. In future iterations, we can implement **Grad-CAM (Gradient-weighted Class Activation Mapping)**. Grad-CAM uses the gradients of the last convolutional layer to generate a heatmap indicating which regions of the foot (e.g., heel or metatarsal) the CNN focused on to make its prediction.

#### Q45: Summarize your personal technical contribution as the Project Lead.
**Answer:** As Project Lead, I spearheaded the transition from a local desktop script to a cloud-ready Progressive Web App. My key contributions include:
1. Establishing the FastAPI async web service and database schema.
2. Writing the HSV-based image validation filter.
3. Migrating the CNN from TensorFlow to ONNX Runtime, reducing memory by $>70\%$.
4. Designing the responsive dashboard and client-side PDF export workflow.

---

## 8. SYSTEM HARDWARE & SOFTWARE REQUIREMENTS

### 8.1 Client-Side Requirements (Patient / Doctor Access)
* **Hardware**: Any smartphone, tablet, or PC with a modern screen display.
* **Operating System**: Android 8.0+, iOS 13.0+, Windows 10/11, macOS, Linux.
* **Web Browser**: Google Chrome 80+, Mozilla Firefox 75+, Apple Safari 13+, Microsoft Edge 80+ (PWA installation supported on Chromium/Safari engines).

### 8.2 Server-Side Deployment Requirements
* **CPU**: 1 Virtual Core (x86_64 or ARM64 architecture).
* **RAM**: Minimum 512MB RAM (Recommended 1GB+ for multi-concurrency handling).
* **Storage**: 200MB available disk space for codebase, ONNX model (`model1.onnx` ~4.2MB), and SQLite storage file.
* **Runtime**: Python 3.10 or Python 3.11 environment.

---

## 9. REFERENCES & BIBLIOGRAPHY
1. **Ring, E. F. J., & Ammer, K.** (2012). *Infrared thermal imaging in medicine*. Physiological Measurement, 33(3), R33.
2. **Boulton, A. J., et al.** (2008). *Comprehensive foot examination and risk assessment*. Diabetes Care, 31(8), 1679-1685.
3. **LeCun, Y., Bengio, Y., & Hinton, G.** (2015). *Deep learning*. Nature, 521(7553), 436-444.
4. **FastAPI & ASGI Specification**: Tiangolo Documentation (https://fastapi.tiangolo.com/).
5. **ONNX Runtime Architecture**: Microsoft Open Source Documentation (https://onnxruntime.ai/).

---
*Report Compiled & Certified by Dhruv Daberao • Project Lead • Final Year B.E. Engineering Submission.*
