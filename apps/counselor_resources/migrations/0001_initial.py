# Generated by Django 5.1.3 on 2024-11-20 02:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherResource',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('image', models.ImageField(blank=True, null=True, upload_to='other_resource/')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('resource_file', models.FileField(blank=True, null=True, upload_to='')),
                ('resource_link', models.URLField(blank=True, null=True)),
                ('resource_type', models.CharField(blank=True, choices=[('ARTICLE', 'article'), ('VIDEO', 'video'), ('AUDIO', 'audio'), ('EBOOK', 'ebook'), ('RESEARCH PAPER', 'research paper'), ('THESIS', 'thesis')], max_length=100, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('is_published', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'other_resource',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CounselorResource',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text="Unique id for a model's object", primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text="Is the model's object active")),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text="Creation date of the model's object")),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text="Updating date of the model's object")),
                ('image', models.ImageField(blank=True, null=True, upload_to='counselor_resource/')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('resource_file', models.FileField(blank=True, null=True, upload_to='')),
                ('resource_link', models.URLField(blank=True, null=True)),
                ('resource_type', models.CharField(blank=True, choices=[('ARTICLE', 'article'), ('VIDEO', 'video'), ('AUDIO', 'audio'), ('EBOOK', 'ebook'), ('RESEARCH PAPER', 'research paper'), ('THESIS', 'thesis')], max_length=100, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'pending'), ('APPROVED', 'approved'), ('REJECTED', 'rejected')], default='PENDING', max_length=100, null=True)),
                ('is_published', models.BooleanField(blank=True, default=False, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_resource', to='user_profile.counselorprofilemodel')),
            ],
            options={
                'db_table': 'counselor_resource',
                'ordering': ['-created_at'],
            },
        ),
    ]
