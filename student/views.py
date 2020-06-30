from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Student
from django.http import HttpResponse, HttpResponseRedirect

# Views
def studentDashboard(request):
    return HttpResponse("here in dashboard")

def registerStudent(request):

    user = request.user
    if Student.objects.filter(user = user).exists() :
        return HttpResponseRedirect('/student/studentDashboard')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        return HttpResponseRedirect('/studentDashboard')
    
    context = {'form' : form}
    template = 'authentication/sign_up.html'
    return render(request,template,context)

