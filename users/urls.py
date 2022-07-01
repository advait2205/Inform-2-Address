from django.urls import path
from users import views

urlpatterns = [
    path('', views.login),
    path('logout', views.logout),
    path('citizen/', views.show_categories),
    path('citizen/<str:category>/complains', views.categorywise_complaints),
    path('citizen/<str:category>/add_complain', views.add_complain),
]