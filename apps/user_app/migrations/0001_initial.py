# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-30 02:22
from __future__ import unicode_literals

import apps.user_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, validators=[apps.user_app.models.validateLengthGreaterThanTwo])),
                ('last_name', models.CharField(max_length=255, validators=[apps.user_app.models.validateLengthGreaterThanTwo])),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('user_level', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]