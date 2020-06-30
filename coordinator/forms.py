from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coordinator, Companies


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields=[
            'name',
            'admissionNumber',
            'branch',
            'yearOfGraduation',
            'rollNumber',
            'course',
        ]

class CompaniesForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields=[
            'name',
            'dateOfVisit',
            'CTC',
            'status',
            'branchesAllowed',
            'CGPA',
        ]
    def __init__(self,*args,**kwargs):
        super(CompaniesForm,self).__init__(*args,**kwargs)
        self.fields['dateOfVisit'].required=False
		