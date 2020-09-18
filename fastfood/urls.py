from django.urls import path
from fastfood.views import get_product_by_id, get_product, upload_data, log_in, get_img

urlpatterns = [
    path('get/<int:pid>', get_product_by_id),
    path('get', get_product),
    path('upload', upload_data, name="upload_data_fastfood"),
    path('login', log_in, name='login_fastfood'),
    path('img', get_img)
]
