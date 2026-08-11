document.addEventListener('DOMContentLoaded', () => {
    
    // --- Navigation / SPA Routing ---
    const navLinks = document.querySelectorAll('.nav-link');
    const viewSections = document.querySelectorAll('.view-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            viewSections.forEach(v => v.classList.remove('active'));

            // Add active class to clicked link
            link.classList.add('active');
            
            // Show corresponding section
            const targetId = link.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            if(targetSection) {
                targetSection.classList.add('active');
            }
        });
    });

    // --- File Upload Simulation ---
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = dropZone.querySelector('.primary-btn');
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.querySelector('.progress-text');
    const fileNameDisplay = document.querySelector('.file-name');

    // Trigger file input click
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and Drop Events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if(files.length > 0) {
            const file = files[0];
            simulateUpload(file.name);
        }
    }

    function simulateUpload(fileName) {
        dropZone.style.display = 'none';
        uploadProgress.style.display = 'block';
        fileNameDisplay.textContent = fileName;
        
        let progress = 0;
        progressBar.style.width = '0%';
        progressText.textContent = `Processing OCR... 0%`;

        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                progressBar.style.width = '100%';
                progressText.textContent = `Extraction Complete! Redirecting to Coding view...`;
                progressText.style.color = 'var(--success)';
                
                // Simulate transition to next phase after a short delay
                setTimeout(() => {
                    // Reset upload view
                    dropZone.style.display = 'block';
                    uploadProgress.style.display = 'none';
                    progressBar.style.width = '0%';
                    progressText.style.color = 'var(--text-muted)';
                    
                    // Navigate to Coding View
                    document.querySelector('.nav-link[data-target="coding"]').click();
                }, 1500);
            } else {
                progressBar.style.width = `${progress}%`;
                progressText.textContent = `Processing OCR... ${Math.round(progress)}%`;
            }
        }, 300);
    }
});
