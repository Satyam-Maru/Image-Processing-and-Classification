from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from imix import processing_tools as tools
from imix import classifier
import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO

def homepage(request):
    return render(request, 'imix/index.html')

def img_classify(request):

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image'].read()  # Get the uploaded image

        # Process the image as needed (without saving)
        # image_name = uploaded_image.name  # Just an example, use it as required

        # image = Image.open(uploaded_image)
        # buffer = BytesIO()
        # image.save(buffer, format=image.format)
        # image_base64 = base64.b64encode(buffer.getvalue()).decode()

        np_img = np.frombuffer(uploaded_image, np.uint8)  # Convert to NumPy array
        image_new = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Decode image

        prediction = classifier.get_prediction(image_new)

        # Pass base64 string to template
        # image_data = f"data:image/{uploaded_image.content_type.split('/')[-1]};base64,{image_base64}"

        return render(request, 'imix/img_classification.html', 
                      { 'scroll_height': 50, 'prediction': prediction})

    return render(request, 'imix/img_classification.html', {'scroll_height': 50})

@csrf_exempt
def img_process(request):
    if request.method == "POST":
        button_id = None
        processed_image = None

        # Handle button click (AJAX request)
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                button_id = data.get("button_id", None)
                print(f"Clicked Button ID: {button_id}")
                request.session["button_id"] = button_id
                return JsonResponse({"message": f"Received button ID: {button_id}"})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Handle image upload
        if "image" in request.FILES:
            image_file = request.FILES["image"].read()  # Read image into memory
            np_img = np.frombuffer(image_file, np.uint8)  # Convert to NumPy array
            image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Decode image

            # Get button ID from session (if available)
            button_id = request.session.get("button_id")

            if button_id and image is not None:
                # Use processing_tools for image processing
                if button_id == "grayscale":
                    processed_image = tools.grayscale(image)
                elif button_id == "resize":
                    pass
                elif button_id == "blur":
                    processed_image = tools.apply_blur(image)
                elif button_id == "edge_detection":
                    processed_image = tools.detect_edges(image)
                elif button_id == "threshold":
                    processed_image = tools.apply_threshold(image)
                elif button_id == "morphology":
                    processed_image = tools.apply_morphology(image)
                elif button_id == "brightness":
                    processed_image = tools.adjust_brightness(image)
                elif button_id == "adjust_rgb":
                    pass
                elif button_id == "plot_rgb":
                    pass

            if processed_image is not None:
                    # Encode processed image to return as response
                _, buffer = cv2.imencode(".jpg", processed_image)
                return HttpResponse(buffer.tobytes(), content_type="image/jpeg")
            else:
                    print("Processed image is None.")
        else:
                print("Button ID or image is missing.")
    return render(request, "imix/img_processing.html", {"scroll_height": 50})