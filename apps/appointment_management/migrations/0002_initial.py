# Generated by Django 5.1.3 on 2024-11-20 01:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointment_management', '0001_initial'),
        ('schedule_management', '0001_initial'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentrequest',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_request', to='user_profile.clientprofilemodel'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='counselor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='counselor_request', to='user_profile.counselorprofilemodel'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_schedule', to='schedule_management.counselorschedule'),
        ),
    ]
