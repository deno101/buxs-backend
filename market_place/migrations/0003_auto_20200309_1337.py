# Generated by Django 2.2.3 on 2020-03-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0002_auto_20200309_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaceproducts',
            name='date_epoch',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='marketplaceproducts',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='marketplaceproducts',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='marketplaceproducts',
            name='price',
            field=models.CharField(default='', max_length=50),
        ),
    ]
