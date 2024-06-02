# Generated by Django 5.0.6 on 2024-06-02 13:23

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("hospital", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BloodTest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "detection_status",
                    models.CharField(
                        choices=[("P", "Pending"), ("C", "Completed"), ("F", "Failed")],
                        default="P",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="BloodTestImageData",
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
                ("image", models.ImageField(upload_to="lab/data-images")),
                (
                    "blood_test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="lab.bloodtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=255)),
                ("birth_date", models.DateField()),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patients",
                        to="hospital.hospital",
                    ),
                ),
            ],
            options={
                "ordering": ["first_name", "last_name"],
            },
        ),
        migrations.AddField(
            model_name="bloodtest",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blood_tests",
                to="lab.patient",
            ),
        ),
        migrations.CreateModel(
            name="Address",
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
                ("street", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                (
                    "patient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="lab.patient"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("description", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "bloodtest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="lab.bloodtest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResultImageData",
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
                ("image", models.ImageField(upload_to="lab/result-images")),
                (
                    "result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="result_images",
                        to="lab.result",
                    ),
                ),
            ],
        ),
    ]
