from django.urls import path
from users import views

urlpatterns = [
    path('', views.show_categories),
    path('login', views.login),
    path('<str:category>/complains', views.categorywise_complaints),
    path('<str:category>/add_complain', views.add_complain),
]