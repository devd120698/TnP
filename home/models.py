from django.db import models
from django.core.validators import FileExtensionValidator

class Links(models.Model):
    twitter = models.URLField(null = True);
    facebook = models.URLField(null = True);
    instagram = models.URLField(null = True);
    gplus = models.URLField(null = True);
    linkedin = models.URLField(null = True);


class PhotosNitw(models.Model):
    photo = models.FileField(null = True,upload_to = 'images/PhotosNITW/',validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg'])])
    caption = models.CharField(null = True, max_length = 50)

class pastRecruiters(models.Model):
    photo = models.FileField(null = True,upload_to = 'images/Recruiters/',validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg'])])

class FrequentlyAsked(models.Model):
<<<<<<< HEAD
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
=======
    question = models.CharField(max_length = 10000)
    answer = models.CharField(max_length = 10000)
>>>>>>> 8a1723023e82c786b958ac0d97aa4d2d0d2fc824

class Team(models.Model):
    name = models.CharField(max_length = 20)
    quote = models.CharField(max_length = 50)
    branch = models.CharField(max_length = 30)
    picture = models.FileField(null = True,upload_to = 'images/Team/',validators=[FileExtensionValidator(allowed_extensions=['png','jpg', 'jpeg'])])




