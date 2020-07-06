from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import Student
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from coordinator.models import Companies

# Views
@login_required
def studentDashboard(request):
    print(CompanyApplicants.objects.all())
    student = Student.objects.get(user = request.user)
    return render(request, 'student/dashboard/index.html', {'student':student})

@login_required
def registerStudent(request):
    user = request.user
    if Student.objects.filter(user = user).exists() :
        HttpResponseRedirect(studentDashboard)

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        HttpResponseRedirect(studentDashboard)
    return render(request,'authentication/form.html',{'form' : form})

@login_required
def viewNewApplications(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).filter(placementStatus = 'N')
    context = {'eligibleCompanies' : company, 'student':student}
    companyName = request.POST.get('nameOfCompany')
    print(companyName, "hello")
    if companyName != None :
        companyDetails = Companies.objects.get(name = companyName)
        applicantData = CompanyApplicants.objects.get(student = student, company = companyDetails)
        applicantData.placementStatus = 'A'
        applicantData.save()
        
    return render(request,'student/showCompanies.html',context)

@login_required
def viewStatusOfApplication(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).exclude(placementStatus = 'N').exclude(placementStatus = 'R')
    return render(request,'student/showApplied.html',{'eligibleCompanies':company, 'student':student})

@login_required
def viewProfile(request):
    resumeUploaded = False
    student = Student.objects.get(user = request.user)
    if Resume.objects.filter(user = request.user).exists():
        resumeUploaded = True
    return render(request,'student/dashboard/pages/profile.html',{'student':student, 'resumeUploaded': resumeUploaded})

@login_required
def uploadResume(request):
    form = ResumeForm(request.POST or None)
    student = Student.objects.get(user = request.user)
    if form.is_valid():
        education = form.cleaned_data.get('educationAll')
        projectAll = form.cleaned_data.get('projectAll')
        acheievementsAll = form.cleaned_data.get('acheievementsAll')
        relevantCoursesAll = form.cleaned_data.get('relevantCoursesAll')
        skillsAll = form.cleaned_data.get('skillsAll')
        extraCurricularAll = form.cleaned_data.get('extraCurricularAll')

        saveDetails = Resume(
            education = education,
            projects = projectAll,
            achievements = acheievementsAll,
            skills = skillsAll,
            relevantCourses = relevantCoursesAll,
            extraCurricular = extraCurricularAll
        )

        saveDetails.save()
    return render(request,'student/Resume.html',{'form':form, 'student':student})    

@login_required
def showCalendar(request):
    student = Student.objects.get(user = request.user)
    return render(request,'student/dashboard/pages/calendar.html',{'student':student})

