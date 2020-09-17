from django.urls import path
from mpesa_pay.views import Lipa_na_mpesa_online, call_back

urlpatterns = [
    path('callback', call_back, name="call_back"),
    path('lipa_na_mpesa', Lipa_na_mpesa_online.as_view(), name="lipa_na_mpesa")
]