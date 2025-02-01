from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.

def homepage(request):
    return render(request, 'imix/index.html')

# def img_process(request):
#     return render(request, 'imix/img_processing.html', {'scroll_height': 50})

def img_classify(request):
    return render(request, 'imix/img_classification.html')

def img_process(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        
        # Save the image to the filesystem (you can also save it in a model or perform other actions)
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)  # Get the URL of the uploaded image
        print(filename)
        print('yes you reached there!')
        # Pass the image URL to the template so it can be displayed
        return render(request, 'imix/img_processing.html', {'file_url': file_url})

    return render(request, 'imix/img_processing.html', {'scroll_height': 50})