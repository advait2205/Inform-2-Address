from django.shortcuts import render

import authority

# Create your views here.

def login(request):
    return render(request, "login.html")

def add_authority(request):
    return render(request, "add_authority.html")