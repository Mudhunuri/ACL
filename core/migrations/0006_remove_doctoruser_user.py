# Generated by Django 4.2.1 on 2024-04-21 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_doctoruser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctoruser',
            name='user',
        ),
    ]