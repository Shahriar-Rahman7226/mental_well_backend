# Generated by Django 5.1.3 on 2024-11-24 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_management', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselorschedule',
            name='is_available',
        ),
    ]