from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Student
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

@login_required
def studentDashboard(request):
    return redirect("/accounts/logout")

@login_required
def registerStudent(request):
    user = request.user
    if Student.objects.filter(user = user).exists() :
    	return redirect("/student/studentDashboard")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
    return render(request, 'authentication/sign_up.html', {'form': form})
