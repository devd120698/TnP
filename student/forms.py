from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student


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
        ]

class ViewCompaniesForm(forms.Form):
    nameOfComany = forms.CharField(max_length=100)