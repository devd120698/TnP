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
from django.contrib.auth.models import AbstractUser

class WSDCStudentRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == StudentUser or model == StudentData:
            return 'wsdc_student'
        return 'default'

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == StudentUser or model == StudentData:
            return 'wsdc_student'
        return 'default'


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the feedback app is involved.
        """
        if obj1._meta.app_label == 'coordinator' or \
           obj2._meta.app_label == 'coordinator':
           return True
        if obj1._meta.app_label == 'student' or \
           obj2._meta.app_label == 'student':
           return True
        return None

    


class StudentUser(AbstractUser):
	ip_address = models.CharField(max_length=15)
	username = models.CharField(unique=True, max_length=100)
	password = models.CharField(max_length=255)
	profile_edited = models.IntegerField(default=1 , blank= True , null=True )
	salt = models.CharField(max_length=40, blank=True, null=True)
	email = models.CharField(unique=True, max_length=100)
	activation_code = models.CharField(max_length=40, blank=True, null=True)
	forgotten_password_code = models.CharField(max_length=40, blank=True, null=True)
	forgotten_password_time = models.PositiveIntegerField(blank=True, null=True)
	remember_code = models.CharField(max_length=40, blank=True, null=True)
	created_on = models.PositiveIntegerField(default =1 ,blank =True,null = True)
	last_login = models.DateTimeField(blank=True, null=True)
	active = models.PositiveIntegerField(blank=True, null=True)
	first_name = models.CharField(max_length=50, blank=True, null=True)
	middle_name = models.CharField(max_length=256)
	last_name = models.CharField(max_length=50, blank=True, null=True)
	company = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=20, blank=True, null=True)

	class Meta:
		db_table = 'users'

	def get_student_data(self):
		return StudentData.objects.using('wsdc_student').filter(userid=self.id).first()

	def get_student_name(self):
		return StudentData.objects.using('wsdc_student').get(userid=self.id).name.split(' ')[0]

	def get_image(self):
		img = StudentData.objects.using('wsdc_student').get(userid=self.id).profile_image

		if img:
			return img.url
		else:
			return "/static/assets/img/person.png"



class Student(models.Model):
    
    
    name = models.CharField(max_length = 120,null=True)
    user = models.ForeignKey(StudentUser,on_delete=models.CASCADE,)
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

    @staticmethod
    def getstudcgpa(self):

        return self.CGPA
  
'''
    Co-ordinator 
    Fields : Name , Reg_No (PK)
'''
class Coordinator(models.Model):
    name =  models.CharField(max_length = 120,null=True)
    registration_number = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'coordinators'

    def __str__(self) : 
        return str(self.registration_number)

 ###
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
    student = models.ForeignKey(StudentUser, on_delete = models.CASCADE, null = True)
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
        return str(self.student.first_name)

    @staticmethod
    def getCompanyName(self):
        return self.company.name

    @staticmethod
    def getStudentName(self):
        return self.student.CGPA
    

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

    user = models.ForeignKey(StudentUser, null = True, on_delete=models.CASCADE)
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
    user = models.ForeignKey(StudentUser, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length = 120)
    mailid = models.EmailField()
    message = models.CharField(max_length = 1000)  

class StudentData(models.Model):
	userid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	roll_number = models.CharField(unique=True, max_length=10, blank=True, null=True)
	registration_number = models.CharField(unique=True, max_length=10, blank=True, null=True)
	current_section = models.CharField(max_length=4)
	current_year = models.CharField(max_length=4)
	joining_year = models.CharField(max_length=4)
	admissiontype = models.CharField(max_length=50, null=True)
	course = models.CharField(max_length=10)
	branch = models.CharField(max_length=10)
	gender = models.CharField(max_length=1)
	birthday = models.DateField()
	country = models.CharField(max_length=32)
	mobile = models.CharField(max_length=16)
	emergency_contact = models.CharField(max_length=16)
	sbh_account = models.CharField(max_length=32, blank=True, null=True)
	passport = models.CharField(max_length=20, blank=True, null=True)
	hostel_room = models.CharField(max_length=10)
	hostel = models.CharField(max_length=10)
	mess = models.CharField(max_length=10)
	created_location = models.CharField(max_length=32)
	created_time = models.DateTimeField()
	guardian1 = models.CharField(max_length=64, blank=True, null=True)
	relationship1 = models.CharField(max_length=64, blank=True, null=True)
	email1 = models.CharField(max_length=64, blank=True, null=True)
	mobile1 = models.CharField(max_length=16, blank=True, null=True)
	guardian2 = models.CharField(max_length=64, blank=True, null=True)
	relationship2 = models.CharField(max_length=64, blank=True, null=True)
	email2 = models.CharField(max_length=64, blank=True, null=True)
	mobile2 = models.CharField(max_length=16, blank=True, null=True)
	homenumber = models.CharField(max_length=16, blank=True, null=True)
	address = models.CharField(max_length=500, blank=True, null=True)
	bloodgroup = models.CharField(max_length=5, blank=True, null=True)
	adhaar = models.CharField(max_length=20, blank=True, null=True)
	linkedin = models.CharField(max_length=100, blank=True, null=True)
	mac = models.CharField(max_length=30, blank=True, null=True)
	profile_image = models.CharField(max_length=200, blank=True, null=True)



	class Meta:
		managed = False
		db_table = 'student_data'
		unique_together = (('roll_number', 'registration_number'),)
