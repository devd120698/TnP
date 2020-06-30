from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.models import User, Group
from student.models import Student
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CompaniesForm
from .models import Companies

# Views

@login_required
def coordinatorDashboard(request):
    user = request.user
    listOfCoordinators = User.objects.filter(groups__name = 'Coordinator')
    emails = User.objects.filter(is_active=True).values_list('email', flat=True).filter(groups__name = 'Coordinator')
    if emails.filter(email = request.user.email).exists() :
        
        #add companies to the list
        form = CompaniesForm(request.POST or None)
        if form.is_valid():
            appl = form.save(commit = False)
            appl.user = request.user
            appl.save()
            return HttpResponse("successful")
        
        context = {'form' : form}
        template = 'authentication/form.html'
        return render(request,template,context)

    else:
        return HttpResponse("unauthorized")

@login_required
def registerCoordinator(request):
    user = request.user
    listOfCoordinators = User.objects.filter(groups__name = 'Coordinator')
    emails = User.objects.filter(is_active=True).values_list('email', flat=True).filter(groups__name = 'Coordinator')
    if emails.filter(email = request.user.email).exists() :
        return HttpResponseRedirect('/coordinator/coordinatorDashboard')

    else:
        return HttpResponse("unauthorized")

