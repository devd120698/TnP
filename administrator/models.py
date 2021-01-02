from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
# from student.models import StudentUser
# Create your models here.
class Administrator(models.Model):
    user = models.OneToOneField('student.StudentUser', related_name='administrator', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name + self.user.last_name

    class Meta:
        db_table = 'administrator_user'


@receiver(post_save, sender=Administrator)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        my_group = Group.objects.get(name='Administrator')
        administrator = Administrator.objects.get_or_create(user=kwargs.get('instance').user)
        my_group.user_set.add(administrator[0].user)

class Course(models.Model):
    
    course = models.CharField(max_length=50,null=False, default = "CSE", primary_key=True)

    def __str__(self):
        return self.course

class Branch(models.Model):

    branch = models.CharField(max_length=50,null=False, default = "CSE")
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    branchCode = models.CharField(max_length = 10,null=False, default = 'cse')

    def __str__(self):
        return self.branch

