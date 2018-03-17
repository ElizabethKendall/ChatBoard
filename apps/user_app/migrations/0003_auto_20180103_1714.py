# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-04 01:14
from __future__ import unicode_literals

import apps.user_app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_auto_20171229_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, validators=[apps.user_app.models.validateLengthGreaterThanTwo, django.core.validators.RegexValidator(regex='^[A-Za-z]\\w+$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, validators=[apps.user_app.models.validateLengthGreaterThanTwo, django.core.validators.RegexValidator(regex='^[A-Za-z]\\w+$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100, validators=[apps.user_app.models.validateLengthGreaterThanTwo]),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], default=1),
        ),
    ]
