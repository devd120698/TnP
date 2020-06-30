from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone

class Student(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    name = models.CharField(max_length=200,null = True)
    admissionNumber = models.IntegerField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    yearOfGraduation = models.IntegerField(null=False)
    rollNumber = models.IntegerField(null=False)
    CGPA = models.FloatField(null=False)
    
    BTECH = 'BT'
    MTECH = 'MT'
    MCA = 'MC'
    MSC = 'MS'
    MBA = 'MB'

    COURSE_CHOICES = (
        (BTECH, 'B. Tech'),
        (MTECH, 'M. Tech'),
        (MCA, 'MCA'),
        (MSC, 'M. Sc'),
        (MBA, 'MBA')
    )

    course = models.CharField(
        max_length=2,
        choices=COURSE_CHOICES,
        default=BTECH,
    )

    def __str__(self) :
        return str(self.admissionNumber)

    class Meta:
        db_table = 'student_user'

@receiver(post_save, sender=Student)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        my_group = Group.objects.get(name='Student')
        student = Student.objects.get(user=kwargs.get('instance').user)
        my_group.user_set.add(student.user)


class Company(models.Model):
    name = models.CharField(max_length=30, blank=False)
    coordinators = models.ManyToManyField(Student)
    branches = models.ManyToManyField(Branch)

    def __str__(self):
        return str(self.name)

class Event(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    time = models.DateTimeField()
    text = models.CharField(max_length=500)
    datePublished = models.DateTimeField(default=timezone.now)

class Announcement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    datePublished = models.DateTimeField(default=timezone.now)
