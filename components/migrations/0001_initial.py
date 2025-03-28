# Generated by Django 5.1.7 on 2025-03-17 20:14

import components.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('product_image', models.ImageField(blank=True, null=True, upload_to=components.models.upload_to_images)),
                ('location_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('datasheet', models.FileField(blank=True, null=True, upload_to=components.models.upload_to_datasheets)),
            ],
        ),
    ]
