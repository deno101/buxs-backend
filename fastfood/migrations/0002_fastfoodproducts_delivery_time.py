# Generated by Django 2.2.3 on 2020-09-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fastfood', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fastfoodproducts',
            name='delivery_time',
            field=models.IntegerField(default=60),
        ),
    ]
