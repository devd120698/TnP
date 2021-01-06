from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from coordinator.models import *

class DateInput(forms.DateInput):
    input_type = 'date'




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
    nameOfCompany = forms.CharField(max_length=100)

class UploadResume(forms.ModelForm):
    class Meta:
        model = Resume
        fields=[
            'resume'
        ]




### Coordinator Forms ### 
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields=[
            'name',
            'registration_number',
        ]




class CompaniesForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(CompaniesForm,self).__init__(*args,**kwargs)
        self.fields['dateOfVisit'].required=False
        self.fields['companyID'].required=False
    class Meta:
        model = Companies
        fields=[
            'name',
            'dateOfVisit',
            'status',
            'branchesAllowed',
            'CGPA',
            'companyID',
            'other_fields_url',
        ]
#widgets
        widgets = {
            'dateOfVisit': DateInput(),
            'branchesAllowed' : forms.HiddenInput(),
        }




    

    


class PlacedCompany(forms.Form):
    
    
    
    def __init__(self, *args, **kwargs):
        super(PlacedCompany, self).__init__(*args, **kwargs)
        companies = Companies.objects.all()
        company_list = []
        company_list.append(('' , '--------'))
        company_list.append(('All Companies','All Companies'))
        for company in companies :
            company_list.append((company.name , company.name))
        COMPANIES = tuple(company_list)
        self.fields['name'].choices = COMPANIES

    name = forms.ChoiceField(choices=[])



class SearchCompany(forms.Form):
    
    
    
    def __init__(self, *args, **kwargs):
        super(SearchCompany, self).__init__(*args, **kwargs)
        companies = Companies.objects.all()
        company_list = []
        company_list.append(('' , '--------'))
        for company in companies :
            company_list.append((company.name , company.name))
        COMPANIES = tuple(company_list)
        self.fields['name'].choices = COMPANIES

    name = forms.ChoiceField(choices=[])

    

class UpdatePlacementStatsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UpdatePlacementStatsForm, self).__init__(*args, **kwargs)
        companies = Companies.objects.all()
        company_list = []
        company_list.append(('' , '--------'))
        for company in companies :
            company_list.append((company.name , company.name))
        COMPANIES = tuple(company_list)
        self.fields['company'].choices = COMPANIES

    company = forms.ChoiceField(choices=[])
    student_roll = forms.CharField(max_length=10)
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
    def __init__(self, *args, **kwargs):
        super(UpdateAnnouncementForm, self).__init__(*args, **kwargs)
        announcements = Announcement.objects.all()
        announcement_list = []
        announcement_list.append(('','--------'))
        for a in announcements :
            announcement_list.append((a.announcementid , a.announcementid))


        ANNOUNCEMENTS = tuple(announcement_list)
        self.fields['announcementid'].choices = ANNOUNCEMENTS
    

    announcementid = forms.ChoiceField(choices=[])
    text = forms.CharField(max_length=20000)
    BROADCAST_ANNOUNCEMENT = 'Broadcasting'
    ELIGIBLE_ANNOUNCEMENT = 'Eligible'
    TYPE_OF_ANNOUNCEMENT = (
        (BROADCAST_ANNOUNCEMENT, 'Broadcast'),
        (ELIGIBLE_ANNOUNCEMENT, 'Eligible_ones'),
    )
    type_of_announcement = forms.ChoiceField(choices = TYPE_OF_ANNOUNCEMENT)



