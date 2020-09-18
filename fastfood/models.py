from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class FastFoodProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='')
    price = models.CharField(max_length=50, default='')
    date_epoch = models.CharField(max_length=100, default='')
    category = models.CharField(max_length=50, default='')

    # product  require three images
    image_url1 = models.CharField(max_length=100, default='')
    image_url2 = models.CharField(max_length=100, default='')
    image_url3 = models.CharField(max_length=100, default='')
    delivery_time = models.IntegerField(default=60)

    description = models.CharField(max_length=10000, default='')

