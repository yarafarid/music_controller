# Generated by Django 5.0.6 on 2025-02-25 09:54

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="code",
            field=models.CharField(
                default=api.models.generate_unique_code, max_length=8, unique=True
            ),
        ),
    ]
