# Generated by Django 5.0.6 on 2024-05-20 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloodtest',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['first_name', 'last_name']},
        ),
    ]
