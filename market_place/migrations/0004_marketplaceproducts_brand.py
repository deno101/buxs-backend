# Generated by Django 2.2.3 on 2020-03-10 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0003_auto_20200309_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaceproducts',
            name='brand',
            field=models.CharField(default='', max_length=100),
        ),
    ]
