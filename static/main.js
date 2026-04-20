let currentUser = JSON.parse(localStorage.getItem('diabetes_user')) || null;
let healthChart = null;

// Initialize Session on Load
document.addEventListener('DOMContentLoaded', () => {
    if (currentUser) {
        document.getElementById('user-display-name').textContent = currentUser.fullname.split(' ')[0];
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('app-section').classList.remove('hidden');
        
        const lastView = localStorage.getItem('diabetes_view') || 'prediction';
        showView(lastView);
    }
    
    // Close modal on outside click
    window.onclick = (e) => {
        const modal = document.getElementById('auth-modal');
        if (e.target === modal) closeAuthModal();
    };
});

// UI State Management
function toggleAuth() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const title = document.getElementById('auth-title');
    const subtitle = document.getElementById('auth-subtitle');

    loginForm.classList.toggle('hidden');
    registerForm.classList.toggle('hidden');

    if (loginForm.classList.contains('hidden')) {
        title.textContent = 'Join the platform';
        subtitle.textContent = 'Create an account to start tracking';
    } else {
        title.textContent = 'Welcome back';
        subtitle.textContent = 'Sign in to your health dashboard';
    }
}

function showView(viewName) {
    localStorage.setItem('diabetes_view', viewName);
    ['prediction', 'analysis', 'remedy', 'profile'].forEach(v => {
        document.getElementById(`${v}-view`).classList.add('hidden');
    });
    document.getElementById(`${viewName}-view`).classList.remove('hidden');
    
    // Update active nav links (Sidebar)
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
        if(link.textContent.toLowerCase().includes(viewName)) link.classList.add('active');
    });

    // Update active nav links (Bottom Nav)
    document.querySelectorAll('.bottom-nav .nav-link').forEach(link => {
        link.classList.remove('active');
        if(link.textContent.toLowerCase().includes(viewName) || 
           (viewName === 'prediction' && link.textContent.includes('Prediction'))) {
            link.classList.add('active');
        }
    });

    if (viewName === 'profile') loadProfileData();
    if (viewName === 'analysis') loadAnalysisHistory();
}

// Authentication
document.getElementById('login-form').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch('/api/auth/login', { method: 'POST', body: formData });
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('diabetes_user', JSON.stringify(currentUser));
            document.getElementById('user-display-name').textContent = currentUser.fullname.split(' ')[0];
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('app-section').classList.remove('hidden');
            showView('prediction');
        } else {
            alert('Invalid credentials');
        }
    } catch (err) {
        console.error(err);
    }
};

document.getElementById('register-form').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
        const response = await fetch('/api/auth/register', { method: 'POST', body: formData });
        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            toggleAuth();
        } else {
            alert('Registration failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (err) {
        console.error(err);
        alert('Registration failed. Please check your connection.');
    }
};

function logout() {
    currentUser = null;
    localStorage.removeItem('diabetes_user');
    localStorage.removeItem('diabetes_view');
    document.getElementById('app-section').classList.add('hidden');
    document.getElementById('auth-section').classList.remove('hidden');
}

// Auth Modal Functions
function openAuthModal() {
    document.getElementById('auth-modal').classList.remove('hidden');
}

function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
}

function selectAuthOption(type) {
    const input = document.querySelector('#login-form input[name="username"]');
    input.placeholder = `Enter your ${type}`;
    input.focus();
    closeAuthModal();
}

// User Profile Management
function loadProfileData() {
    if (!currentUser) return;
    document.getElementById('prof-fullname').value = currentUser.fullname;
    document.getElementById('prof-age').value = currentUser.age;
    document.getElementById('prof-email').value = currentUser.email;
    document.getElementById('prof-phone').value = currentUser.phone;
    document.getElementById('prof-username').value = currentUser.username;
    document.getElementById('prof-password').value = currentUser.password;
}

function toggleProfileEdit() {
    const isEdit = document.getElementById('edit-profile-btn').textContent === 'Edit Profile';
    const fields = ['fullname', 'age', 'email', 'phone', 'password'];
    
    fields.forEach(f => {
        document.getElementById(`prof-${f}`).readOnly = !isEdit;
    });

    document.getElementById('edit-profile-btn').textContent = isEdit ? 'Cancel' : 'Edit Profile';
    document.getElementById('save-profile-btn').classList.toggle('hidden');
}

document.getElementById('profile-form').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    formData.append('current_username', currentUser.username);
    formData.append('address', ''); // Keep field for DB compatibility but empty

    try {
        const response = await fetch('/api/profile/update', { method: 'POST', body: formData });
        if (response.ok) {
            alert('Profile updated successfully!');
            currentUser.fullname = formData.get('fullname');
            currentUser.email = formData.get('email');
            currentUser.phone = formData.get('phone');
            currentUser.age = formData.get('age');
            currentUser.password = formData.get('password');
            
            toggleProfileEdit();
            loadProfileData();
        }
    } catch (err) {
        console.error(err);
    }
};

function togglePasswordVisibility(id) {
    const field = document.getElementById(id);
    const icon = document.getElementById(id + '-icon');
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Stepper Workflow
function updateStepper(step) {
    // Handle Circles
    document.querySelectorAll('.step').forEach((el, index) => {
        el.classList.remove('active', 'done');
        const sNum = index + 1;
        
        // Reset to default dark blue
        const circle = el.querySelector('.step-circle');
        circle.style.backgroundColor = 'var(--primary-dark)';
        circle.style.borderColor = 'var(--primary-dark)';

        if (sNum <= step) {
            circle.style.backgroundColor = 'var(--success)';
            circle.style.borderColor = 'var(--success)';
            el.classList.add('done');
        }
        if (sNum === step) el.classList.add('active');
    });

    // Handle Lines
    document.querySelectorAll('.stepper-line').forEach((el, index) => {
        el.classList.remove('active');
        if (index + 1 < step) el.classList.add('active');
    });

    document.querySelectorAll('.step-content').forEach((el, index) => {
        el.classList.add('hidden');
        if (index + 1 === step) el.classList.remove('hidden');
    });
}

function resetStepper() {
    document.getElementById('image-upload').value = '';
    document.getElementById('file-name').textContent = 'No file selected';
    updateStepper(1); // Set to step 1 (Upload) but circle 1 remains dark until upload
    
    // Explicit reset for circle 1 on re-entry
    const c1 = document.querySelector('#step-1 .step-circle');
    c1.style.backgroundColor = 'var(--primary-dark)';
    c1.style.borderColor = 'var(--primary-dark)';
}

document.getElementById('image-upload').onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('prev-orig').src = URL.createObjectURL(file);
        updateStepper(2);
    }
};

// Global state for current analysis
let currentResultData = null;

async function runPrediction() {
    const fileInput = document.getElementById('image-upload');
    const btn = document.getElementById('predict-btn');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    btn.disabled = true;
    btn.textContent = 'Processing Pipeline...';

    try {
        const response = await fetch('/api/predict', { method: 'POST', body: formData });
        
        // Check for common server-side crash status codes (like 502 Bad Gateway)
        if (response.status === 502 || response.status === 504) {
            throw new Error(`Cloud server crashed or timed out (Error ${response.status}). This usually happens when the free tier runs out of memory (RAM).`);
        }

        let data;
        try {
            data = await response.json();
        } catch (jsonErr) {
            const rawBody = await response.text();
            console.error('Non-JSON Response:', rawBody);
            throw new Error('Server returned an invalid response. The server may have run out of memory.');
        }

        if (response.ok && data.status === 'success') {
            currentResultData = data;
            document.getElementById('diagnosis-text').textContent = data.prediction;
            document.getElementById('confidence-text').textContent = `Confidence Score: ${data.confidence}%`;
            document.getElementById('confidence-bar').style.width = (parseFloat(data.confidence) * 100) + '%';
            
            const grayImg = document.getElementById('prev-gray');
            const threshImg = document.getElementById('prev-thresh');
            
            // Set sources with cache-busting
            const timestamp = Date.now();
            grayImg.src = data.visuals.gray + '?v=' + timestamp;
            threshImg.src = data.visuals.threshold + '?v=' + timestamp;
            
            // Safety: Handle potential load failures
            const fallback = (el) => { el.src = ''; el.alt = 'Analysis Image Not Ready'; };
            grayImg.onerror = () => fallback(grayImg);
            threshImg.onerror = () => fallback(threshImg);
            
            updateStepper(3);
        } else {
            console.error('Analysis Error:', data);
            alert(`Analysis failed: ${data.detail || 'Unknown server error'} (Status: ${response.status})`);
        }
    } catch (err) {
        console.error('Fetch Error:', err);
        alert(`Analysis failed: ${err.message || 'Could not connect to the server'}`);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Run CNN Analysis';
    }
}

async function saveCurrentResult() {
    if (!currentResultData || !currentUser) return;
    
    const formData = new FormData();
    formData.append('username', currentUser.username);
    formData.append('prediction', currentResultData.prediction);
    formData.append('confidence', currentResultData.confidence);
    formData.append('image_path', currentResultData.visuals.original);

    const btn = document.getElementById('save-result-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';

    try {
        const response = await fetch('/api/analysis/save', { method: 'POST', body: formData });
        if (response.ok) {
            btn.innerHTML = '<i class="fa-solid fa-check"></i> Saved';
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save Result';
            }, 2000);
        }
    } catch (err) {
        console.error(err);
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-bookmark"></i> Save Result';
    }
}

async function loadAnalysisHistory() {
    if (!currentUser) return;
    const list = document.getElementById('analysis-history-list');
    const empty = document.getElementById('analysis-empty-state');
    
    try {
        const response = await fetch(`/api/analysis/list?username=${currentUser.username}`);
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            empty.classList.add('hidden');
            list.innerHTML = data.history.map(item => `
                <div class="history-card">
                    <div class="history-info">
                        <span class="history-prediction">${item.prediction}</span>
                        <span class="history-meta">Confidence: ${item.confidence}%</span>
                        <div class="history-timestamp">
                            <span class="history-meta"><i class="fa-regular fa-calendar"></i> ${item.date}</span>
                            <span class="history-meta"><i class="fa-solid fa-calendar-day"></i> ${item.day}</span>
                            <span class="history-meta"><i class="fa-regular fa-clock"></i> ${item.time || '--:--'}</span>
                        </div>
                    </div>
                    <div class="history-img-wrapper">
                        <img src="${item.image_path}" alt="Screening">
                    </div>
                    <button class="delete-btn" title="Delete record" onclick="deleteHistory(${item.id})">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            `).join('');
            
            calculateTrends(data.history);
            renderChart(data.history);
        } else {
            empty.classList.remove('hidden');
            list.innerHTML = '';
            document.getElementById('trend-banner').classList.add('hidden');
        }
    } catch (err) {
        console.error(err);
    }
}

function calculateTrends(history) {
    const banner = document.getElementById('trend-banner');
    const status = document.getElementById('trend-status');
    const advice = document.getElementById('trend-advice');
    const icon = document.getElementById('trend-icon');
    
    if (history.length < 2) {
        banner.classList.add('hidden');
        return;
    }

    banner.classList.remove('hidden');

    // Score: Not At Risk = 1, At Risk = 0
    const scores = history.map(h => h.prediction.includes('Not') ? 1 : 0).reverse();
    const latest = scores[scores.length - 1];
    const previous = scores[scores.length - 2];
    const avgRecent = scores.slice(-3).reduce((a, b) => a + b, 0) / Math.min(scores.length, 3);
    const avgPast = scores.slice(0, -3).reduce((a, b) => a + b, 0) / Math.max(scores.length - 3, 1);

    if (avgRecent >= avgPast) {
        banner.className = 'card mb-4 trend-banner improving';
        status.textContent = 'Health Trend: Improving';
        advice.textContent = 'Keep it up, your metrics are showing positive progress! Continue your current diet.';
        icon.className = 'fa-solid fa-arrow-trend-up';
    } else {
        banner.className = 'card mb-4 trend-banner worsening';
        status.textContent = 'Health Trend: Worsening';
        advice.textContent = 'You need to take better care of your glucose levels. Please review your diet plan.';
        icon.className = 'fa-solid fa-arrow-trend-down';
    }
}

function renderChart(history) {
    const ctx = document.getElementById('healthChart').getContext('2d');
    const data = [...history].reverse();
    
    if (healthChart) healthChart.destroy();

    healthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(h => h.date),
            datasets: [{
                label: 'Health Score (1=Safe, 0=Risk)',
                data: data.map(h => h.prediction.includes('Not') ? 1 : 0),
                borderColor: '#1e3a8a',
                backgroundColor: 'rgba(30, 58, 138, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: '#1e3a8a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: -0.2, max: 1.2, ticks: { display: false }, grid: { display: false } },
                x: { 
                    grid: { display: false },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 6,
                        maxRotation: 45,
                        minRotation: 0,
                        font: { size: 10 }
                    }
                }
            },
            plugins: { 
                legend: { display: false },
                tooltip: { backgroundColor: '#1e3a8a' }
            }
        }
    });
}

function downloadPDF() {
    if (!currentUser) return;
    
    const element = document.getElementById('analysis-report-content');
    const opt = {
        margin: [10, 10],
        filename: `ClinicalReport_${currentUser.username}_${new Date().getTime()}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    // Show a loading state
    const btn = document.querySelector('button[onclick="downloadPDF()"]');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating PDF...';

    html2pdf().set(opt).from(element).save().then(() => {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }).catch(err => {
        console.error('PDF Generation Error:', err);
        btn.disabled = false;
        btn.innerHTML = originalText;
        alert('Failed to generate PDF. Please try again.');
    });
}

async function deleteHistory(id) {
    if (!confirm('Are you sure you want to delete this record?')) return;
    try {
        const response = await fetch(`/api/analysis/delete/${id}`, { method: 'DELETE' });
        if (response.ok) loadAnalysisHistory();
    } catch (err) {
        console.error(err);
    }
}
