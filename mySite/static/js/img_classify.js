const uploadContainer = document.getElementById('upload-container');
const fileInput = document.getElementById('file-input');
const browseSection = document.getElementById('browse-section');
const preview = document.getElementById('preview');
const browseAgainContainer = document.getElementById('browse-again-container');
const resetButton = document.getElementById('reset-button');

// Handle drag-and-drop events
uploadContainer.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadContainer.classList.add('dragover');
});

uploadContainer.addEventListener('dragleave', () => {
    uploadContainer.classList.remove('dragover');
});

uploadContainer.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadContainer.classList.remove('dragover');
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleFiles(files[0]);
    }
});

// Handle file input change
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        handleFiles(file);
    }
});

// Function to handle image file
function handleFiles(file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            browseSection.style.display = 'none'; // Hide the browse section
            preview.style.display = 'block'; // Show the preview section
            preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" class="img-fluid">`;
            browseAgainContainer.style.display = 'block'; // Show the "Browse Again" button
            addResetButtonListener(); // Attach listener to the reset button
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please upload a valid image file.');
    }
}

// Function to reset the view
function resetView() {
    fileInput.value = ''; // Reset the file input
    preview.style.display = 'none'; // Hide the preview section
    browseSection.style.display = 'block'; // Show the browse section
    browseAgainContainer.style.display = 'none'; // Hide the "Browse Again" button  
}

// Attach event listener to the reset button
function addResetButtonListener() {
    resetButton.addEventListener('click', resetView);
}

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const previewDiv = document.getElementById("preview");
    const browseSection = document.getElementById("browse-section");

    if (!fileInput || !previewDiv || !browseSection) {
        console.error("One or more elements missing!");
        return; // Stop execution if elements are not found
    }

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewDiv.innerHTML = `<img src="${e.target.result}" class="img-fluid" style="max-width: 100%; height: auto;">`;
                previewDiv.style.display = "block";
                browseSection.style.display = "none"; // Hide browse section
            };
            reader.readAsDataURL(file);
        }
    });

    // If an image already exists (from Django), hide the browse section
    if (previewDiv.innerHTML.trim() !== "") {
        browseSection.style.display = "none";
    }
});
