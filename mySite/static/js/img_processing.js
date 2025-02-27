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
originalImageBase64 = "";
window.base64_arr = [];

// Function to handle image file
function handleFiles(file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            originalImageBase64 = e.target.result;
            currentImageBase64 = originalImageBase64;
            base64_arr.push(currentImageBase64);
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
    originalImageBase64 = "";
    base64_arr = [];
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

window.renderSlider = function (buttonValue) {
    const sliderSection = document.getElementById('slider-section');
    sliderSection.innerHTML = ''; // Clear previous content

    let sliderHTML = '';
    console.log('inside the renderSlider()');

    switch (buttonValue) {
        case 'grayscale':
            sliderHTML = `
                <div class="form-group">
                    <label for="grayscale">Intensity</label> <br>
                    <input type="range" class="form-control-range custom-slider" id="grayscale" min="0.1" max="5.0" step="0.1" value="1">
                    <span id="grayscale-value" style="display: inline-block; width: 40px; text-align: center;">1</span>
                </div>
            `;
            break;

        case 'resize':
            sliderHTML = `
                <div class="form-group">
                    <label for="width-input">Width</label>
                    <input type="number" class="form-control custom-slider dark-input" id="width-input" min="100" max="1024" value="500">
                </div>
                <div class="form-group">
                    <label for="height-input">Height</label>
                    <input type="number" class="form-control custom-slider dark-input" id="height-input" min="100" max="1024" value="500">
                </div>
            `;
            break;

        case 'blur':
            sliderHTML = `
                    <div class="form-group">
                        <label for="blur">Kernel size (Intensity) </label> <br>
                        <input type="range" class="form-control-range custom-slider" id="blur" min="3" max="15" step="2" value="5">
                        <span id="blur-value" style="display: inline-block; width: 40px; text-align: center;">5</span>
                    </div>
                `;
            break;

        case 'edge_detection':
            sliderHTML = `
                    <div class="form-group">
                        <label for="edge_detection">Threshold value</label> <br>
                        <input type="range" class="form-control-range custom-slider" 
                            id="edge_detection" min="10" max="150" step="10" value="50">
                        <span id="edge_detection-value" style="display: inline-block; width: 40px; text-align: center;">50</span>
                    </div>
                `;
            break;

        case 'erode':

        case 'dilate':

        case 'morphology':
            sliderHTML = `
                    <div class="form-group">
                    <button class="btn btn-outline-warning morph-btn" 
                    onclick="sendButtonID(this.value)" type="button" id="erode-btn" value="erode">Erode</button>
                    <button class="btn btn-outline-warning morph-btn"
                    onclick="sendButtonID(this.value)" type="button" id="dilate-btn" value="dilate">Dilate</button>
                    </div>
                `;
            break;

        case 'brightness':
            sliderHTML = `
                    <div class="form-group">
                        <label for="brightness">Brightness</label> <br>
                        <input type="range" class="form-control-range custom-slider" 
                            id="brightness" min="-100" max="100" step="5" value="0">
                        <span id="brightness-value" style="display: inline-block; width: 40px; text-align: center;">0</span>
                    </div>
                `;
            break;

        default:
            sliderHTML = `<p>No options available for this tool.</p>`;
    }

    sliderSection.innerHTML = sliderHTML;

    function updateSliderValue(event) {
        const slider = event.target;
        const valueDisplay = document.getElementById(`${slider.id}-value`);
        if (valueDisplay) {
            valueDisplay.textContent = slider.value;
        }
    }

    // Attach event listeners to all sliders dynamically
    document.querySelectorAll('.custom-slider').forEach(slider => {
        slider.addEventListener('input', updateSliderValue);
    });

    const morphButtons = document.querySelectorAll(".morph-btn");

    morphButtons.forEach(button => {
        button.addEventListener("click", function () {

            morphButtons.forEach(btn => {
                btn.classList.remove("btn-warning");
                btn.classList.add("btn-outline-warning");
            });

            this.classList.remove("btn-outline-warning");
            this.classList.add("btn-warning");
        });
    });
};

document.getElementById('undo-btn').addEventListener('click', function () {

    if (!currentImageBase64) {
        alert('Please upload an image first!');
        return;
    }

    // Contains only original image uploaded
    if(base64_arr.length == 1){
        alert('Please apply atleast one filter!')
        return;
    }

    base64_arr.pop(); // Remove the existing image
    currentImageBase64 = base64_arr[base64_arr.length - 1]; // Previous image
    document.getElementById("preview").innerHTML = `<img src="${currentImageBase64}" class="img-fluid"/>`;
});

document.getElementById('reset-btn').addEventListener('click', function () {

    if (!currentImageBase64) {
        alert('Please upload an image first!');
        return;
    }

    currentImageBase64 = originalImageBase64;
    base64_arr = [];
    base64_arr.push(currentImageBase64);
    document.getElementById("preview").innerHTML = `<img src="${currentImageBase64}" class="img-fluid"/>`;
});