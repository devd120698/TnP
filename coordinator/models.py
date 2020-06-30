from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone

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
