from django.urls import path
from . import views

urlpatterns = [
    path('gdata/', views.get_mp),
    path('img/', views.get_img),
    path('login/', views.log_in, name='login'),
    path('updata/', views.upload_data, name='uplaod'),
]