from django import forms
from .models import LoginDetails, Schedule, SelectedStudents
from django.core.validators import FileExtensionValidator

class LoginDetailsForm(forms.ModelForm):
    class Meta:
        model = LoginDetails
        fields = [
            # 'user',
			'name',
			'uploadFile',
		]

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            # 'user',
			'name',
			'uploadFile',
		]

class SelectedStudentsForm(forms.Form):
    
    name = forms.CharField(max_length = 10)
    uploadFile = forms.FileField()
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        roundDetails = SelectedStudents.getRounds(self.user)
        roundsArray = roundDetails.split(",")
        ROUND_CHOICES = ()        
        for round in roundsArray:
            ROUND_CHOICES +=(round,round),
        print(ROUND_CHOICES)
        super(SelectedStudentsForm, self).__init__(*args, **kwargs)
        self.fields['round'] = forms.ChoiceField(
            choices=ROUND_CHOICES
        )

