# Generated by Django 3.0.8 on 2020-07-10 05:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200706_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastrecruiters',
            name='photo',
            field=models.FileField(null=True, upload_to='images/Recruiters/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='photosnitw',
            name='photo',
            field=models.FileField(null=True, upload_to='images/PhotosNITW/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='team',
            name='picture',
            field=models.FileField(null=True, upload_to='images/Team/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
    ]