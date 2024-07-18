# Generated by Django 5.0.6 on 2024-07-15 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lab", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resultimagedata",
            name="image",
        ),
        migrations.AddField(
            model_name="resultimagedata",
            name="image_urls",
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]