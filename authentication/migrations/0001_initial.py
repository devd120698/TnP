# Generated by Django 3.1.4 on 2021-01-01 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
            ],
        ),
    ]
