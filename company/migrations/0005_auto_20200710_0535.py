# Generated by Django 3.0.8 on 2020-07-10 05:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20200707_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logindetails',
            name='uploadFile',
            field=models.FileField(null=True, upload_to='images/Documents/Company/LoginDetails', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='uploadFile',
            field=models.FileField(null=True, upload_to='images/Documents/Company/Schedule', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
