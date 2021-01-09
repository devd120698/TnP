from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group 
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from company.models import Details
from student.models import *




# class Coordinator(models.Model):
    
#     name = models.CharField(max_length = 120,null=True)
#     user = models.ForeignKey('student.StudentUser',on_delete=models.CASCADE,)
#     admissionNumber = models.IntegerField(primary_key=True)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     yearOfGraduation = models.IntegerField(null=False)
#     rollNumber = models.IntegerField(null=False)
    
#     BTECH = 'BT'
#     MTECH = 'MT'
#     MCA = 'MC'
#     MSC = 'MS'
#     MBA = 'MB'

#     COURSE_CHOICES = (
#         (BTECH, 'B. Tech'),
#         (MTECH, 'M. Tech'),
#         (MCA, 'MCA'),
#         (MSC, 'M. Sc'),
#         (MBA, 'MBA')
#     )

#     course = models.CharField(
#         max_length=2,
#         choices=COURSE_CHOICES,
#         default=BTECH,
#     )

#     def __str__(self) :
#         return str(self.admissionNumber)


# @receiver(post_save, sender=Coordinator)
# def ensure_profile_exists(sender, **kwargs):
#     if kwargs.get('created', False):
#         my_group = Group.objects.get(name='Coordinator')
#         coordinator = Coordinator.objects.get(user=kwargs.get('instance').user)
#         my_group.user_set.add(coordinator.user)

class Companies(models.Model):
    
    COMPANY_STATUS = (
        ('Yet to Fill CPNF', 'Yet to fill CPNF'),
        ('CPNF received, unscheduled', 'CPNF received, unscheduled'),
        ('OT scheduled', 'OT scheduled'),
        ('Interview scheduled' , 'Interview scheduled'),
        (' Results received' , ' Results received')
    )
    name = models.CharField(max_length = 120, primary_key=True)
    dateOfVisit = models.DateField(null = True)
    status = models.CharField(
        max_length=100,
        choices=COMPANY_STATUS,
        default='Yet to Fill CPNF',
    )
    ALIVE = 'Alive'
    DEAD = 'Dead'
    EXISTING_STATUS = (
        (ALIVE, 'Alive'),
        (DEAD, 'Dead'),
    )
    existing_status = models.CharField(
        max_length=100,
        choices=EXISTING_STATUS,
        default=ALIVE,
    )
    branchesAllowed = models.CharField(max_length=2000, blank=True, null=True,default='')

    other_fields_url = models.URLField(max_length=200,default='',null=True,blank=True)

    CGPA = models.FloatField(null=False, default = 7.0)
    companyID = models.ForeignKey(Details,on_delete = models.CASCADE, null = True)

    def __str__(self) :
        return str(self.name)

class Announcement(models.Model):
    BROADCAST_ANNOUNCEMENT = 'Broadcasting'
    ELIGIBLE_ANNOUNCEMENT = 'Eligible'
    TYPE_OF_ANNOUNCEMENT = (
        (BROADCAST_ANNOUNCEMENT, 'Broadcast'),
        (ELIGIBLE_ANNOUNCEMENT, 'Eligible_ones'),
    )
    type_of_announcement = models.CharField(
        max_length=20,
        choices=TYPE_OF_ANNOUNCEMENT,
        default=BROADCAST_ANNOUNCEMENT,
    )
    announcementid = models.CharField(max_length = 120, primary_key=True)
    user = models.IntegerField( null =False)
    datePublished = models.DateField(default=timezone.now)
    text = models.TextField(max_length=500)
    company = models.ForeignKey(Companies,on_delete = models.CASCADE, null = True)

    def __str__(self) :
        return str(self.announcementid)

    @staticmethod
    def getCompanyName(self):
        return self.company.name


