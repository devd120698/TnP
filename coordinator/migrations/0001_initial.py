# Generated by Django 3.0.7 on 2020-06-30 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrator', '0002_branch'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('name', models.CharField(max_length=120, null=True)),
                ('admissionNumber', models.IntegerField(primary_key=True, serialize=False)),
                ('yearOfGraduation', models.IntegerField()),
                ('rollNumber', models.IntegerField()),
                ('course', models.CharField(choices=[('BT', 'B. Tech'), ('MT', 'M. Tech'), ('MC', 'MCA'), ('MS', 'M. Sc'), ('MB', 'MBA')], default='BT', max_length=2)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
