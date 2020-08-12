from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import StudentRegisterForm
from home.models import *
from company.forms import ContactForm
from django.core.mail import send_mail

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.forms import *
from student.models import *
from django.core.mail import send_mail
from django.http import HttpResponse
import bcrypt

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

def get_student_data(username, password):
    # Checking is student or not
    user = StudentUser.objects.using('wsdc_student').filter(Q(username=username) | Q(email=username))

    if len(user) == 0:
        stud_data = StudentData.objects.using('wsdc_student').filter(registration_number=username).first()
        if stud_data is not None:
            user = StudentUser.objects.using('wsdc_student').filter(id=stud_data.userid)

    if len(user) != 0:
        return user.get()
    else:
        return None

def sign_in(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        student_user = get_student_data(username, password)
        user =None
        # user = authenticate(username=username, password=password)
        if user is None and student_user is None:
            return render(request, 'Tnp_home/index.html', {'error': 'Invalid username or password'})
        else:
            try:
                if student_user is not None:
                    if bcrypt.checkpw(password.encode('utf-8'), student_user.password.encode('utf-8')):
                        login(request, student_user, backend='django.contrib.auth.backends.ModelBackend')
                        try:
                            student = StudentData.objects.using('wsdc_student').get(userid=request.user.id)
                        except StudentData.DoesNotExist:
                            return render(request, 'Tnp_home/index.html', {'error': 'Invalid username or password'})
                    return redirect('student/studentDashBoard/')
                
                # Code comes here if student_user is not found.
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if is_coordinator(request.user):
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