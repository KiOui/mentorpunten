# Generated by Django 4.2.3 on 2023-08-11 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0002_file_compressed_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompressionRequested",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="compression_requested",
                        to="files.file",
                    ),
                ),
            ],
        ),
    ]