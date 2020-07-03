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
    websiteLink = models.CharField(max_length = 120, null=True)
    hrDetails = models.CharField(max_length = 20000, null=True)
    address = models.CharField(max_length = 20000, null=True)
    emailId = models.EmailField(null=True)
    phoneNumber = models.CharField(max_length = 15,null=True)
    mobileNumber = models.CharField(max_length = 15,null=True) 
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

    jobDesignation = models.CharField(max_length = 120, null=True)
    jobType = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')
    workLocation = models.CharField(max_length = 1000, null=True)
    # otherInfo = models.CharField(max_length = 10000, null=True)
    tentativeDOJ = models.DateField(null =True)
    roundsDetails = models.CharField(validators=[validate_comma_separated_integer_list],max_length=20000, blank=True, null=True,default='')
    numberOfRounds = models.CharField(max_length = 10,null=True)
    otherInfo = models.CharField(max_length = 1000, null=True)
    
    salaryDetails_btech = models.CharField(max_length = 1000)
    salaryDetails_mtech = models.CharField(max_length = 1000)
    salaryDetails_otherPG = models.CharField(max_length = 1000)
    salaryDetails_PhD = models.CharField(max_length = 1000)
    minOffers = models.CharField(max_length = 10, null=True, default = '0')

    trainingPeriod = models.CharField(max_length = 10,null=True, default = '0')
    stipulatedBond = models.CharField(max_length = 10,null=True, default = 0)

    stipendDetails_BTech = models.CharField(max_length = 1000)
    stipendDetails_MTech = models.CharField(max_length = 1000)
    stipendDetails_OtherPG = models.CharField(max_length = 1000)

    duration_UG = models.CharField(max_length = 1000)
    duration_PG = models.CharField(max_length = 1000)



    



