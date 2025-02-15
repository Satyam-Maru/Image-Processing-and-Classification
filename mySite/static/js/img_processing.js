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

window.currentImageBase64 = "";

// Function to handle image file
function handleFiles(file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            currentImageBase64 = e.target.result;
            // console.log(typeof currentImageBase64);
            browseSection.style.display = 'none'; // Hide the browse section
            preview.style.display = 'block'; // Show the preview section
            preview.innerHTML = `<img src="${currentImageBase64}" alt="Uploaded Image" class="img-fluid">`;
            // console.log(`this is original image ${e.target.result}`);
            browseAgainContainer.style.display = 'block'; // Show the "Browse Again" button
            addResetButtonListener(); // Attach listener to the reset button
            
            document.getElementById("imageBase64").value = currentImageBase64; // Remove "data:image/png;base64,"
            console.log('you got into handleFiles()')
    };
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
    currentImageBase64 = "";
}

// Attach event listener to the reset button
function addResetButtonListener() {
    resetButton.addEventListener('click', resetView);
}

/* Capture mouse position */
document.querySelectorAll(".tool-btn").forEach(button => {
    button.addEventListener("mousemove", (e) => {

        let rect = button.getBoundingClientRect();
        button.style.setProperty("--x", `${e.clientX - rect.left}px`);
        button.style.setProperty("--y", `${e.clientY - rect.top}px`);
    });

    button.addEventListener("click", (e) => {
        // Prevents the default action of the button (like submitting a form or page reload)
        e.preventDefault();
        
        // Print the button's value (text content) to the console
        console.log(button.textContent.trim());  // .trim() to remove any extra spaces

        // Remove 'selected' class from all buttons
        document.querySelectorAll(".tool-btn").forEach(btn => {
            btn.classList.remove('selected');
        });

        // Add 'selected' class to the clicked button
        button.classList.add('selected');
    });
});

document.getElementById("slider").addEventListener("input", function () {
    document.getElementById("sliderValue").innerText = this.value;
});
