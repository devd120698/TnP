from django.db import models
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from django.core.validators import FileExtensionValidator

class Details(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, default = "", null =True)
    name = models.CharField(max_length = 120,primary_key = True, default = 'ABC')
    websiteLink = models.CharField(max_length = 120, null=True)
    hrDetails = models.CharField(max_length = 20000, null=True)
    address = models.CharField(max_length = 20000, null=True)
    emailId = models.EmailField(null=True)
    phoneNumber = models.CharField(max_length = 15,null=True)
    mobileNumber = models.CharField(max_length = 15,null=True) 
    sector = models.CharField(validators=[validate_comma_separated_integer_list],max_length=2000, blank=True, null=True,default='')
    category = models.CharField(validators=[validate_comma_separated_integer_list],max_length=2000, blank=True, null=True,default='')
    jobDesignation = models.CharField(max_length = 120, null=True)
    jobType = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')
    workLocation = models.CharField(max_length = 1000, null=True)
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

    def __str__(self):
        return self.name

class LoginDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = "", null = True)
    uploadFile = models.FileField(null = True,upload_to = 'test/Documents/Company/LoginDetails',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    name = models.CharField(max_length = 10, default = "name")
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = "", null = True)
    uploadFile = models.FileField(null = True,upload_to = 'test/Documents/Company/Schedule',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    name = models.CharField(max_length = 10, default = "name")
    
    def __str__(self):
        return self.name

class SelectedStudents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadFile = models.FileField(null = True,upload_to = 'test/Documents/Company/Schedule',validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    name = models.CharField(max_length = 10)
    DUMMY = 'D'
    ROUND_CHOICE = (
        (DUMMY, 'D'),
    )

    round = models.CharField(
        max_length=20,
        choices=ROUND_CHOICE,
        default=DUMMY,
    )
    
    def __str__(self):
        return self.name

    @staticmethod
    def getRounds(user):
        if Details.objects.filter(user=user).exists():
            getCompany = Details.objects.get(user = user)
            return getCompany.companyDetails.values_list('roundDetails', flat=True)[0]
        return "dummy, dummy2, dummy3"

    



