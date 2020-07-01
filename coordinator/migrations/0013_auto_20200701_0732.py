# Generated by Django 3.0.7 on 2020-07-01 07:32

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0012_auto_20200701_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='branchesAllowed',
        ),
        migrations.AddField(
            model_name='companies',
            name='branchesAllowed',
            field=models.CharField(blank=True, default='', max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
