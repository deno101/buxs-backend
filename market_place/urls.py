from django.urls import path
from . import views

urlpatterns = [
    path('gdata/', views.get_mp),
    path('img/', views.get_img),
]