# Generated by Django 5.1.3 on 2024-11-25 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='founderprofilemodel',
            name='is_founder',
        ),
    ]
