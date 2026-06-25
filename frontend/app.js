const imageInput = document.getElementById('image-input');
const uploadArea = document.getElementById('upload-area');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const uploadText = document.getElementById('upload-text');
const presetCards = document.querySelectorAll('.preset-card');
const transformBtn = document.getElementById('transform-btn');
const loadingState = document.getElementById('loading-state');
const errorToast = document.getElementById('error-toast');
const screenInput = document.getElementById('screen-input');
const screenReveal = document.getElementById('screen-reveal');
const originalImg = document.getElementById('original-img');
const transformedImg = document.getElementById('transformed-img');
const vibeRating = document.getElementById('vibe-rating');
const resetBtn = document.getElementById('reset-btn');

let selectedFile = null;
let selectedPreset = null;

// Handle File Upload
imageInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
        selectedFile = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            uploadText.style.display = 'none';
        };
        reader.readAsDataURL(selectedFile);
        checkReadyState();
    }
});

// Handle Preset Selection
presetCards.forEach(card => {
    card.addEventListener('click', () => {
        presetCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        selectedPreset = card.dataset.preset;
        checkReadyState();
    });
});

function checkReadyState() {
    if (selectedFile && selectedPreset) {
        transformBtn.disabled = false;
    } else {
        transformBtn.disabled = true;
    }
}

function showError(msg) {
    errorToast.textContent = msg;
    errorToast.classList.remove('hidden');
    setTimeout(() => {
        errorToast.classList.add('hidden');
    }, 4000);
}

// Handle Transform
transformBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError("Please upload a selfie first!");
        return;
    }
    if (!selectedPreset) {
        document.querySelector('.preset-selector').classList.add('shake');
        setTimeout(() => {
            document.querySelector('.preset-selector').classList.remove('shake');
        }, 500);
        return;
    }

    transformBtn.classList.add('hidden');
    loadingState.classList.remove('hidden');

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('preset_id', selectedPreset);

    try {
        const response = await fetch('/api/transform', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to transform image");
        }

        const data = await response.json();
        
        // Show reveal screen
        originalImg.src = data.original_image_url;
        transformedImg.src = data.transformed_image_url;
        vibeRating.textContent = `Stylist says: "${data.vibe_rating}"`;

        screenInput.classList.add('hidden');
        screenReveal.classList.remove('hidden');

    } catch (err) {
        showError(err.message || "Something went wrong.");
    } finally {
        transformBtn.classList.remove('hidden');
        loadingState.classList.add('hidden');
    }
});

resetBtn.addEventListener('click', () => {
    // Reset state
    selectedFile = null;
    selectedPreset = null;
    imageInput.value = '';
    imagePreview.src = '';
    previewContainer.classList.add('hidden');
    uploadText.style.display = 'block';
    presetCards.forEach(c => c.classList.remove('selected'));
    transformBtn.disabled = true;

    screenReveal.classList.add('hidden');
    screenInput.classList.remove('hidden');
});
