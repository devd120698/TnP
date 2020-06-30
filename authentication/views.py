from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import StudentRegisterForm

#Group checking functions
def is_student(user):
	return user.groups.filter(name='Student').exists()

def is_coordinator(user):
	return user.groups.filter(name='Coordinator').exists()

def is_administrator(user):
	return user.groups.filter(name='Administrator').exists()

def is_superuser(user):
	return user.is_superuser

# Views
def index(request):
	if request.user.is_authenticated and request.user.is_active == True:
		student_flag = is_student(request.user)
		if is_student(request.user):
			return redirect('student/')

		elif is_coordinator(request.user):
			return redirect('coordinator/')

		elif is_administrator(request.user):
			return redirect('administration/')

		elif is_superuser(request.user):
			return redirect('admin/')
		else:
			return render(request, 'authentication/index.html', None)
	else:
		return render(request, 'authentication/index.html', None)


def sign_in(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is None:
			return render(request, 'authentication/index.html', {'error': 'Invalid username or password'})
		else:
			try:
				login(request, user)
				if is_student(request.user):
					return redirect('student/')

				elif is_coordinator(request.user):
					return redirect('coordinator/')

				elif is_administrator(request.user):
					return redirect('administrator/')

				elif is_superuser(request.user):
					return redirect('/admin')

			except:
				return render(request, 'authentication/index.html', {'error': 'Invalid username or password'})
	else:
		return index(request)


# def sign_out(request):
# 	logout(request)
# 	return redirect('/')

# def log_in(request):
# 	return render(request, 'authentication/log_in.html', {})

def about_us(request):
	return render(request, 'authentication/about.html', {})

def contact_us(request):
	return render(request, 'authentication/contact.html', {})

# def sign_up(request):
# 	return render(request, 'authentication/sign_up.html', {})

def sign_up(request):
	if request.method == 'POST':
		form = StudentRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f' Your account has been created !')
			return redirect('student-login')
	else :
		form = StudentRegisterForm()
	return render(request,'authentication/sign_up.html',{'form':form})
