from django.db import models
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list

class Details(models.Model):
    name = models.CharField(max_length = 120,primary_key = True, default = 'ABC')
    websiteLink = models.CharField(max_length = 120, null = False)
    hrDetails = models.CharField(max_length = 20000, null = False)
    address = models.CharField(max_length = 20000, null = False)
    emailId = models.EmailField(null=False)
    phoneNumber = models.IntegerField(null=False)
    mobileNumber = models.IntegerField(null=False) 
    sector = models.CharField(validators=[validate_comma_separated_integer_list],max_length=2000, blank=True, null=True,default='')
    category = models.CharField(validators=[validate_comma_separated_integer_list],max_length=2000, blank=True, null=True,default='')
    
    # SECTOR_CHOICES = (
    #     ("CORE ENGG", "CORE ENGG"),
    #     ("IT", "IT"),
    #     ("CONSULTING", "CONSULTING"),
    #     ("MANUFACTURING", "MANUFACTURING"),
    #     ("FINANCE", "FINANCE"),
    #     ("E-COMMERCE", "E-COMMERCE"),
    #     ("ANALYTICS", "ANALYTICS"),
    #     ("OIL & GAS", "OIL & GAS"),
    #     ("OTHER", "OTHER"),
    # )

    # CATEGORY_CHOICES = (
    #     ("GOVT", "GOVT"),
    #     ("PSU", "PSU"),
    #     ("MNC", "MNC"),
    #     ("LTD", "LTD"),
    #     ("PRIVATE", "PRIVATE"),
    #     ("NGO", "NGO"),
    #     ("OTHER", "OTHER"),
    # )

    # TYPE_CHOICES = (
    #     ("DOMESTIC", "DOMESTIC"),
    #     ("INTERNATIONAL", "INTERNATIONAL"),
    # )

    # sector = models.ManyToManyField(
    #     max_length = 20,
    #     choices = SECTOR_CHOICES,
    #     default="CORE ENGG"
    # )
    # category = models.ManyToManyField(
    #     max_length = 20,
    #     choices = CATEGORY_CHOICES,
    #     default="GOVT"
    # )

    # typeOfPlacement = models.CharField(
    #     max_length = 20,
    #     choices = TYPE_CHOICES,
    #     default="DOMESTIC"
    # )

    jobDesignation = models.CharField(max_length = 120, null = False)
    jobType = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')
    workLocation = models.CharField(max_length = 1000, null = False)
    otherInfo = models.CharField(max_length = 10000, null = False)
    tentativeDOJ = models.DateField(null =False)
    roundsDetails = models.CharField(validators=[validate_comma_separated_integer_list],max_length=20000, blank=True, null=True,default='')
    numberOfRounds = models.IntegerField(null=False)
    otherInfo = models.CharField(max_length = 1000, null = False)
    
    salaryDetails_btech = models.CharField(max_length = 1000)
    salaryDetails_mtech = models.CharField(max_length = 1000)
    salaryDetails_otherPG = models.CharField(max_length = 1000)
    salaryDetails_PhD = models.CharField(max_length = 1000)

    trainingPeriod = models.IntegerField(null=False, default = 0)
    stipulatedBond = models.IntegerField(null=False, default = 0)

    stipendDetails_BTech = models.CharField(max_length = 1000)
    stipendDetails_MTech = models.CharField(max_length = 1000)
    stipendDetails_OtherPG = models.CharField(max_length = 1000)

    duration_UG = models.CharField(max_length = 1000)
    duration_PG = models.CharField(max_length = 1000)



    



