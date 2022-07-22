from django.urls import path
from users import views

urlpatterns = [
    path('', views.show_categories),
    path('citizen/', views.show_categories),
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
    path('citizen/<str:category>/complains', views.categorywise_complaints),
    path('citizen/<str:category>/<int:id>', views.upvote_complain),
    path('citizen/<str:category>/add_complain', views.add_complain),
]