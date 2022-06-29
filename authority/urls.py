from django.urls import path
from authority import views

urlpatterns = [
    path('login', views.login),
    path('add_authority', views.add_authority),
    path('assigned_complains', views.assigned_complains),
]