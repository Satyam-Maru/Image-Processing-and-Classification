from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'imix/index.html')

def img_process(request):
    return render(request, 'imix/img_processing.html', {'scroll_height': 50})

def img_classify(request):
    return render(request, 'imix/img_classification.html')