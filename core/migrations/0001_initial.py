# Generated by Django 4.0.6 on 2022-07-31 22:35

import core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=150, verbose_name='Address')),
                ('state', models.CharField(max_length=50, verbose_name='state')),
                ('zip_code', models.CharField(max_length=10, validators=[core.validators.zip_code_validator], verbose_name='Zip Code')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
