# Generated by Django 5.0.6 on 2024-05-22 07:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid5, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='BloodTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid5, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('detection_status', models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('F', 'Failed')], default='P', max_length=1)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_tests', to='lab.patient')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lab.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid5, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('bloodtest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='lab.bloodtest')),
            ],
        ),
    ]
