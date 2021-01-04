# Generated by Django 2.2 on 2021-01-02 16:35

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coordinator', '0001_initial'),
        ('administrator', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('roll_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('registration_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('current_section', models.CharField(max_length=4)),
                ('current_year', models.CharField(max_length=4)),
                ('joining_year', models.CharField(max_length=4)),
                ('admissiontype', models.CharField(max_length=50, null=True)),
                ('course', models.CharField(max_length=10)),
                ('branch', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=1)),
                ('birthday', models.DateField()),
                ('country', models.CharField(max_length=32)),
                ('mobile', models.CharField(max_length=16)),
                ('emergency_contact', models.CharField(max_length=16)),
                ('sbh_account', models.CharField(blank=True, max_length=32, null=True)),
                ('passport', models.CharField(blank=True, max_length=20, null=True)),
                ('hostel_room', models.CharField(max_length=10)),
                ('hostel', models.CharField(max_length=10)),
                ('mess', models.CharField(max_length=10)),
                ('created_location', models.CharField(max_length=32)),
                ('created_time', models.DateTimeField()),
                ('guardian1', models.CharField(blank=True, max_length=64, null=True)),
                ('relationship1', models.CharField(blank=True, max_length=64, null=True)),
                ('email1', models.CharField(blank=True, max_length=64, null=True)),
                ('mobile1', models.CharField(blank=True, max_length=16, null=True)),
                ('guardian2', models.CharField(blank=True, max_length=64, null=True)),
                ('relationship2', models.CharField(blank=True, max_length=64, null=True)),
                ('email2', models.CharField(blank=True, max_length=64, null=True)),
                ('mobile2', models.CharField(blank=True, max_length=16, null=True)),
                ('homenumber', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('bloodgroup', models.CharField(blank=True, max_length=5, null=True)),
                ('adhaar', models.CharField(blank=True, max_length=20, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True)),
                ('mac', models.CharField(blank=True, max_length=30, null=True)),
                ('profile_image', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'student_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('ip_address', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('profile_edited', models.IntegerField()),
                ('salt', models.CharField(blank=True, max_length=40, null=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('activation_code', models.CharField(blank=True, max_length=40, null=True)),
                ('forgotten_password_code', models.CharField(blank=True, max_length=40, null=True)),
                ('forgotten_password_time', models.PositiveIntegerField(blank=True, null=True)),
                ('remember_code', models.CharField(blank=True, max_length=40, null=True)),
                ('created_on', models.PositiveIntegerField()),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('active', models.PositiveIntegerField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('middle_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('name', models.CharField(max_length=120, null=True)),
                ('registration_number', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'coordinators',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=120, null=True)),
                ('admissionNumber', models.IntegerField()),
                ('yearOfGraduation', models.IntegerField()),
                ('rollNumber', models.IntegerField(primary_key=True, serialize=False)),
                ('CGPA', models.FloatField()),
                ('address', models.TextField(null=True)),
                ('mobileNumber', models.CharField(max_length=10, null=True)),
                ('picture', models.FileField(null=True, upload_to='RegisterPictures/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.Branch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student_user',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(null=True, upload_to='images/Resume', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('text', models.CharField(max_length=500)),
                ('datePublished', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.Companies')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('mailid', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyApplicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placementStatus', models.CharField(choices=[('A', 'Applied'), ('I', 'Qualified for Interview'), ('N', 'Not applied'), ('P', 'Placed'), ('R', 'R')], default='N', max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.Companies')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinator.Companies')),
                ('user', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]