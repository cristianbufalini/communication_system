# Generated by Django 5.0.1 on 2024-01-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mensaje",
            name="archivo_audio",
            field=models.FileField(blank=True, null=True, upload_to="archivos_audio/"),
        ),
    ]