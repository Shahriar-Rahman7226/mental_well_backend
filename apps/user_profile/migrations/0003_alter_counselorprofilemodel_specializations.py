# Generated by Django 5.1.3 on 2024-11-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_remove_founderprofilemodel_is_founder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counselorprofilemodel',
            name='specializations',
            field=models.ManyToManyField(blank=True, null=True, related_name='counselor_specialization', to='user_profile.specializationmodel'),
        ),
    ]
