from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from imix import processing_tools as tools
import cv2
import numpy as np

def homepage(request):
    return render(request, 'imix/index.html')

def img_classify(request):
    return render(request, 'imix/img_classification.html')

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
                print("Processing image using processing_tools...")

                # Use processing_tools for image processing
                if button_id == "grayscale":
                    processed_image = tools.grayscale(image)
                elif button_id == "blur":
                    processed_image = tools.blur(image)
                elif button_id == "edge_detection":
                    processed_image = tools.edge_detection(image)
                # Add more transformations as needed

                if processed_image is not None:
                    # Encode processed image to return as response
                    _, buffer = cv2.imencode(".jpg", processed_image)
                    print("Processed image successfully. Returning image response.")
                    return HttpResponse(buffer.tobytes(), content_type="image/jpeg")
                else:
                    print("Processed image is None.")
            else:
                print("Button ID or image is missing.")
    return render(request, "imix/img_processing.html", {"scroll_height": 50})