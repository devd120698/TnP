from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student_Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created == True:
        Profile.objects.create(user=instance)
        print("profile is created !")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    print('Profile is saved !')






