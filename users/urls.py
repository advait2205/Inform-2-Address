from django.urls import path
from users import views

urlpatterns = [
    path('', views.show_categories),
    path('category', views.categorywise_complaints),
    path('category/add_complain', views.add_complain),
]