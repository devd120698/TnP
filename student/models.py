from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from administrator.models import Branch
from django.utils import timezone
from coordinator.models import Companies
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django.core.validators import FileExtensionValidator
# As model field:
from django_currentuser.db.models import CurrentUserField

class Student(models.Model):
    
    name = models.CharField(max_length = 120,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    admissionNumber = models.IntegerField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    yearOfGraduation = models.IntegerField(null=False)
    rollNumber = models.IntegerField(null=False, primary_key=True)
    CGPA = models.FloatField(null=False)
    address = models.TextField( null = True)
    mobileNumber = models.CharField(max_length = 10, null = True)
    picture = models.FileField(null = True,upload_to = 'RegisterPictures/',validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg'])])

    def __str__(self) :
        return str(self.rollNumber)

    class Meta:
        db_table = 'student_user'

    @staticmethod
    def getUser(self):
        return self.user

@receiver(post_save, sender=Student)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        my_group = Group.objects.get(name='Student')
        student = Student.objects.get(user=kwargs.get('instance').user)
        my_group.user_set.add(student.user)

class Event(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    venue = models.CharField(max_length=100)
    time = models.DateTimeField()
    text = models.CharField(max_length=500)
    datePublished = models.DateTimeField(default=timezone.now)


class Application(models.Model):
    user = CurrentUserField()
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    def __str__(self) :
        student = Student.objects.get(user=self.user)
        return str(student)


class CompanyApplicants(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null = True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    APPLIED = 'A'
    INTERVIEW = 'I'
    NOTAPPLIED = 'N'
    PLACED = 'P'
    REJECTED = 'R'

    APPLICATION_STATUS = (
        (APPLIED, 'Applied'),
        (INTERVIEW, 'Qualified for Interview'),
        (NOTAPPLIED, 'Not applied'),
        (PLACED, 'Placed'),
        (REJECTED, 'R')
    )

    placementStatus = models.CharField(
        max_length=2,
        choices=APPLICATION_STATUS,
        default=NOTAPPLIED,
    )

    def __str__(self):
        return str(self.student.admissionNumber) + " " +self.student.name + " " + self.student.user.email

    @staticmethod
    def getCompanyName(self):
        return self.company.name

    @staticmethod
    def getStudentName(self):
        return self.student.name

class Resume(models.Model):
    
    # name = models.CharField(max_length = 50, null = True)
    # year = models.CharField(max_length = 50, null = True)
    # email = models.EmailField(null = True)
    # phoneNumber = models.CharField(max_length = 15, null = True)
    # address = models.TextField(default = "1234 main st")
    # student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    # education = models.TextField()
    # projects = models.TextField()
    # achievements = models.TextField(null = True)
    # skills = models.TextField(null = True)
    # # fieldOfInterest = models.CharField(max_length = 20000000, null = True)
    # relevantCourses = models.TextField( null = True)
    # extraCurricular = models.TextField( null = True)

    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)
    resume = models.FileField(null = True, upload_to="images/Resume",validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    def __str__(self):
        return str(self.user)
    
    # @staticmethod
    # def getRelevant(self):
    #     return self.relevantCourses

    # @staticmethod
    # def getAchievements(self):
    #     return self.achievements

    # @staticmethod
    # def getExtraCurricular(self):
    #     return self.extraCurricular
    
    # @staticmethod
    # def getSkills(self):
    #     return self.skills
    
    # @staticmethod
    # def getProjects(self):
    #     return self.projects
    
    # @staticmethod
    # def getEducation(self):
    #     return self.education

    

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length = 120)
    mailid = models.EmailField()
    message = models.CharField(max_length = 20000000)  




