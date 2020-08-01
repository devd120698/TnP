from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import StudentRegisterForm
from home.models import *
from company.forms import ContactForm
from django.core.mail import send_mail

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.forms import *
from student.models import *
from django.core.mail import send_mail
from django.http import HttpResponse

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
	# if request.user.is_authenticated and request.user.is_active == True:
	# 	student_flag = is_student(request.user)
	# 	if is_student(request.user):
	# 		return redirect('student/')

	# 	elif is_coordinator(request.user):
	# 		return redirect('coordinator/')

	# 	elif is_administrator(request.user):
    # 			return redirect('administration/')

	# 	elif is_superuser(request.user):
	# 		return redirect('admin/')
	# 	else:
	# 		return render(request, 'home/index.html', None)
	# else:
	# 	return render(request, 'home/index.html', None)

    links = Links.objects.all()
    recruiters = pastRecruiters.objects.all()
    team = Team.objects.all()
    photos = PhotosNitw.objects.all()
    faq = FrequentlyAsked.objects.all()
    form = ContactForm(request.POST or None)

    # new logic!
    if request.method == 'POST':
        name = form.cleaned_data.get('name')
        mailid = form.cleaned_data.get('mailid')
        message = form.cleaned_data.get('message')
        saveDetails = ContactCompany(
            name=name,
            mailid=mailid,
            message=message
        )
        saveDetails.save()
        send_mail(
            name + ' contacting CCPD',
            message,
            'nagamraghu120117143@gmail.com',
            [mailid],
            fail_silently=True,
        )
    context = {'Recruiters':recruiters, 'Team':team, 'CampusPictures': photos, 'FAQs': faq,'form':form}
    return render(request, 'home/index.html', context)

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'Tnp_home/index.html', {'error': 'Invalid username or password'})
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
                return render(request, 'Tnp_home/index.html', {'error': 'Invalid username or password'})
                
    else:
        return index(request)


# def sign_out(request):
# 	logout(request)
# 	return redirect('/')

# def log_in(request):
# 	return render(request, 'authentication/log_in.html', {})

def about_us(request):
	return render(request, 'authentication/resume.html', {})

def contact_us(request):
	return render(request, 'authentication/contact.html', {})

def sign_up(request):
    return render(request,'account/index.html',{})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')