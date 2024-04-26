# Generated by Django 4.2.1 on 2024-04-26 10:23

import core.model.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('experience', models.IntegerField(null=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('degree', models.CharField(blank=True, max_length=15, null=True)),
                ('role', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', core.model.manager.ActiveUserManager()),
            ],
        ),
    ]
