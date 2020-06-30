from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Administrator(models.Model):
    user = models.OneToOneField(User, related_name='administrator', on_delete=models.CASCADE)

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

class Branch(models.Model):
    ComputerScienceEngineering = 'CSE'
    ElectronicsCommunicationEngineering = 'ECE'
    ElectricalElectronicsEngineering = 'ECE'
    MechanicalEngineering = 'ME'
    ChemicalEngineering = 'CHE'
    CivilEngineering = 'CE'
    MetallurgicalMaterialsEngineering = 'MME'
    Biotechnology = 'BIO'
    BRANCH_CHOICES = (
        (ComputerScienceEngineering, 'Computer Science & Engineering'),
        (ElectronicsCommunicationEngineering, 'Electronics & Communication Engineering'),
        (ElectricalElectronicsEngineering, 'Electrical & Electronics Engineering'),
        (MechanicalEngineering, 'Mechanical Engineering'),
        (ChemicalEngineering, 'Chemical Engineering'),
        (CivilEngineering, 'Civil Engineering'),
        (MetallurgicalMaterialsEngineering, 'Metallurgical & Materials Engineering'),
        (Biotechnology, 'Biotechnology'),
    )
    
    branch = models.CharField(
        max_length=3,
        choices=BRANCH_CHOICES,
        default=ComputerScienceEngineering,
    )

    def __str__(self):
        return self.branch



