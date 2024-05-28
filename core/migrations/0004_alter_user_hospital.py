# Generated by Django 5.0.6 on 2024-05-28 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_user_hospital_user_is_hospital_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="hospital",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="core.hospital",
            ),
            preserve_default=False,
        ),
    ]
