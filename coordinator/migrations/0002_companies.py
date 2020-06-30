# Generated by Django 3.0.7 on 2020-06-30 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coordinator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('dateOfVisit', models.DateField()),
                ('CTC', models.IntegerField()),
                ('yearOfGraduation', models.IntegerField()),
                ('rollNumber', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
