# Generated by Django 2.2.3 on 2020-02-29 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buxsbackend', '0002_marketplaceproducts_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaceproducts',
            name='image_url',
            field=models.CharField(default='', max_length=100),
        ),
    ]
