from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coordinator, Companies, Announcement

from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'


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
            'status',
            'branchesAllowed',
            'CGPA',
            'companyID'
        ]
#widgets
        widgets = {
            'dateOfVisit': DateInput(),
        }



    def __init__(self,*args,**kwargs):
        super(CompaniesForm,self).__init__(*args,**kwargs)
        self.fields['dateOfVisit'].required=False
        self.fields['companyID'].required=False
		
class SearchCompany(forms.Form):
    name = forms.CharField(max_length=100)

class UpdatePlacementStatsForm(forms.Form):
    company = forms.CharField(max_length=100)
    students = forms.CharField(max_length=20000)
    APPLIED = 'A'
    INTERVIEW = 'I'
    PLACED = 'P'
    SELECTION_STATUS = (
        (INTERVIEW, 'interview'),
        (PLACED, 'placed'),
        (APPLIED, 'applied'),
    )
    status = forms.ChoiceField(choices = SELECTION_STATUS)

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields=[
            'announcementid',
            'company',
            'text',
            'datePublished',
            'type_of_announcement',
        ]
    def __init__(self,*args,**kwargs):
        super(AnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['datePublished'].required=False

class SearchAnnouncement(forms.Form):
    announcementid = forms.CharField(max_length=10)

class UpdateAnnouncementForm(forms.Form):
    announcementid = forms.CharField(max_length=10)
    text = forms.CharField(max_length=20000)
    BROADCAST_ANNOUNCEMENT = 'Broadcasting'
    ELIGIBLE_ANNOUNCEMENT = 'Eligible'
    TYPE_OF_ANNOUNCEMENT = (
        (BROADCAST_ANNOUNCEMENT, 'Broadcast'),
        (ELIGIBLE_ANNOUNCEMENT, 'Eligible_ones'),
    )
    type_of_announcement = forms.ChoiceField(choices = TYPE_OF_ANNOUNCEMENT) 
 

		