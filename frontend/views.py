from django.shortcuts import render

def index(request, *argts, **kwargs):
    return render(request, 'frontend/index.html') 