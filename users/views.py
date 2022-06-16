from django.shortcuts import render, HttpResponse

# Create your views here.
def show_categories(request):
    return render(request, "index.html")