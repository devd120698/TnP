from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields=[
            'name',
            'admissionNumber',
            'branch',
            'yearOfGraduation',
            'rollNumber',
            'CGPA',
            'address',
            'mobileNumber'
        ]

class ViewCompaniesForm(forms.Form):
    nameOfCompany = forms.CharField(widget = forms.HiddenInput(), required = False,max_length=100)

class UploadResume(forms.ModelForm):
    class Meta:
        model = Resume
        fields=[
            'resume'
        ]

        