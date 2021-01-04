from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User


def index(request):
	return render(request,'administrator/index.html')

def add_company(request):
	return render(request,'administrator/template.html')

