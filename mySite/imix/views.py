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
import re

def homepage(request):
    return render(request, 'imix/index.html')


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
        if json.loads(request.body).get("image"):
            # image_file = request.FILES["image"].read()  # Read image into memory
            # print(request.FILES)
            # np_img = np.frombuffer(image_file, np.uint8)  # Convert to NumPy array
            # image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Decode image
            # print('yes you got the image!')
            # Get button ID from session (if available)
            button_id = request.session.get("button_id")
            print("inside the image_base64 if block")

            # *******************************************************
            #  New section for testing using hidden value in html
            data = json.loads(request.body)
            base64_image = data.get("image")
            # print(base64_image)

            match = re.match(r"data:image/(?P<ext>.*?);base64,(?P<data>.*)", base64_image)
            if not match:
                return JsonResponse({"error": "Invalid Base64 format"}, status=401)

            ext = match.group("ext")  # Get image extension (png, jpeg, etc.)
            base64_data = match.group("data")  # Extract only the Base64 content

            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            image_array = np.array(image)
            image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            # *******************************************************

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
                
                processed_image_base64 = base64.b64encode(buffer).decode("utf-8")
                processed_image_url = f"data:image/jpeg;base64,{processed_image_base64}"
                # print(processed_image_base64)

                return JsonResponse({"image_url": processed_image_url, "base64": processed_image_base64})
            else:
                return JsonResponse({"error": 'hello'}, status=500)
        else:
                return JsonResponse({"error": 'hi'}, status=404)
    return render(request, "imix/img_processing.html", {"scroll_height": 50})

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