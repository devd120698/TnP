from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from company.models import Details
class Coordinator(models.Model):
    
    name = models.CharField(max_length = 120,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    admissionNumber = models.IntegerField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    yearOfGraduation = models.IntegerField(null=False)
    rollNumber = models.IntegerField(null=False)
    
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


@receiver(post_save, sender=Coordinator)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        my_group = Group.objects.get(name='Coordinator')
        coordinator = Coordinator.objects.get(user=kwargs.get('instance').user)
        my_group.user_set.add(coordinator.user)

class Companies(models.Model):
    WAITING = 'Waiting'
    DENIED = 'Denied'
    ACCEPTED = 'Accepted'
    COMPANY_STATUS = (
        (WAITING, 'waiting'),
        (DENIED, 'denied'),
        (ACCEPTED, 'accepted'),
    )
    name = models.CharField(max_length = 120, primary_key=True)
    dateOfVisit = models.DateField(null = True)
    status = models.CharField(
        max_length=8,
        choices=COMPANY_STATUS,
        default=WAITING,
    )
    branchesAllowed = models.CharField(max_length=2000, blank=True, null=True,default='')
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
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    datePublished = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)
    company = models.ForeignKey(Details,on_delete = models.CASCADE, null = True)

    def __str__(self) :
        return str(self.announcementid)


