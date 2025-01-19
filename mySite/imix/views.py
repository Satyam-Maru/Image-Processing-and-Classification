from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'imix/index.html')

def base(request):
    return render(request, 'imix/base.html')