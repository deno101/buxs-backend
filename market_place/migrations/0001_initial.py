# Generated by Django 2.2.3 on 2020-03-06 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketPlaceProducts',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=50)),
                ('date_epoch', models.CharField(max_length=100)),
                ('category', models.CharField(default='', max_length=50)),
                ('image_url', models.CharField(default='', max_length=100)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
