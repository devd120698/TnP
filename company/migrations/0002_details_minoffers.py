# Generated by Django 3.0.8 on 2020-07-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='minOffers',
            field=models.CharField(default='1', max_length=10),
        ),
    ]