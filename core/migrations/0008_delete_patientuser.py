# Generated by Django 4.2.1 on 2024-04-23 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_doctor_delete_doctoruser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatientUser',
        ),
    ]