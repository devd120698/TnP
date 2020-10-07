from django.db import models
from django.utils import timezone
from student.models import StudentUser
from PIL import Image
from django.urls import reverse


class Student_Profile(models.Model):
	user_id = models.IntegerField()
	image = models.ImageField( default = 'default.jpg' , upload_to = 'profile_pics')

	def __str__(self):
		return self.user.username + 'Profile'

	# def save(self, *args, **kwargs):
	# 	super().save()
		
	# 	img = Image.open(self.image.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)
