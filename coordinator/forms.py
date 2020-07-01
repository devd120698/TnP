from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coordinator, Companies, UpdateStudents

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
		
class SearchCompany(forms.Form):
    name = forms.CharField(max_length=100)

class UpdatePlacementStatsForm(forms.Form):
    company = forms.CharField(max_length=100)
    students = forms.CharField(validators=[validate_comma_separated_integer_list],max_length=20000, blank=True, null=True,default='')
		