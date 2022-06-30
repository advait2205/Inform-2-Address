from django.urls import path
from authority import views

urlpatterns = [
    path('login', views.login),
    path('assigned_complains', views.assigned_complains),
]