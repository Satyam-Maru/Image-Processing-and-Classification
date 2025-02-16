from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from imix import processing_tools as tools
from imix import classifier
import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import re

from .forms import CreateUser
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# login / signUp
def registerUser(request):
    form = CreateUser()

    if request.method == 'POST':
        print("POST data:", request.POST)  # Debugging
        form = CreateUser(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging
            user = form.save()
            print("User created:", user)  # Debugging
            return redirect('login')
        else:
            print("Form is invalid")  # Debugging
            print(form.errors)  # Debugging
            # Add form errors to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        print("Request method is not POST")  # Debugging

    context = {'form': form}
    return render(request, 'imix/signup.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            auth_login(request, user)
            print('user logged in')
            return redirect('img_process')  # Redirect to the img_process template
        else:
            # Authentication failed, return an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'imix/login.html', {'error': 'Invalid username or password.'})
    
    # If the request method is GET, just render the login page
    return render(request, 'imix/login.html')

def logout_view(request):
    logout(request)
    return redirect('img_process')  # Redirect to the login page after logout

def homepage(request):
    return render(request, 'imix/index.html')


# main work of backend for processing and classification

# PROCESSING
@login_required
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

            button_id = request.session.get("button_id")
            print("inside the image_base64 if block")

            # *******************************************************
            #  New section for testing using hidden value in html
            data = json.loads(request.body)
            base64_image = data.get("image")
            slider_value = data.get('slider_value')
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
                    processed_image = tools.grayscale(image, beta=int(slider_value))
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
                    processed_image = tools.adjust_brightness(image, beta=int(slider_value))
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

#  CLASSIFICATION
@login_required
def img_classify(request):

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image'].read()  # Get the uploaded image

        np_img = np.frombuffer(uploaded_image, np.uint8)  # Convert to NumPy array
        image_new = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Decode image

        prediction = classifier.get_prediction(image_new)

        return render(request, 'imix/img_classification.html', 
                      { 'scroll_height': 50, 'prediction': prediction})

    return render(request, 'imix/img_classification.html', {'scroll_height': 50})
