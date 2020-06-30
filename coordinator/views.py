from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import Coordinator
from django.http import HttpResponse, HttpResponseRedirect

# Views
def coordinatorDashboard(request):
    return HttpResponse("here in dashboard")

def registerCoordinator(request):

    user = request.user
    if Coordinator.objects.filter(user = user).exists() :
        return HttpResponseRedirect('/coordinator/coordinatorDashboard')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        return HttpResponseRedirect('/coordinator/coordinatorDashboard')
    
    context = {'form' : form}
    template = 'authentication/sign_up.html'
    return render(request,template,context)

