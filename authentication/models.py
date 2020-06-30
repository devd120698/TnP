from django.db import models
<<<<<<< HEAD
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Student_Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField( default = 'default.jpg' , upload_to = 'profile_pics')

	def __str__(self):
		return f'{ self.user.username } Profile'

	# def save(self, *args, **kwargs):
	# 	super().save()
		
	# 	img = Image.open(self.image.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)
=======
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
>>>>>>> master
