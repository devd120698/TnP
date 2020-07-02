# Generated by Django 3.0.8 on 2020-07-02 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_remove_student_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyapplicants',
            name='placementStatus',
            field=models.CharField(choices=[('A', 'Applied'), ('I', 'Qualified for Interview'), ('N', 'Not applied'), ('P', 'Placed'), ('R', 'R')], default='N', max_length=2),
        ),
    ]