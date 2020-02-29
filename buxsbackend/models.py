
from django.db import models
from django.contrib.auth.models import User


class MarketPlaceProducts(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    # owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date_epoch = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='')
    image_url = models.CharField(max_length=100, default='')
