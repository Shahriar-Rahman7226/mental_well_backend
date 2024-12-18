# Generated by Django 5.1.3 on 2024-11-20 01:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('introduction', models.TextField(blank=True, null=True)),
                ('mission', models.TextField(blank=True, null=True)),
                ('vision', models.TextField(blank=True, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'about_us',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BannerModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='banner/')),
            ],
            options={
                'db_table': 'banner_model',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FooterModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('image', models.ImageField(blank=True, null=True, upload_to='footer/')),
                ('details', models.TextField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('emergency_support', models.TextField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'footer_models',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LegalDocument',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('details', models.TextField(blank=True, null=True)),
                ('version', models.CharField(blank=True, max_length=100, null=True)),
                ('licence_document', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'db_table': 'legal_document',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MotivationModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('quote_text', models.TextField(blank=True, null=True)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'motivation_model',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('details', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'privacy_policy',
                'ordering': ['-created_at'],
            },
        ),
    ]
