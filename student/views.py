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
    return render(request, 'student/dashboard/index.html', {})

@login_required
def registerStudent(request):

    user = request.user
    if Student.objects.filter(user = user).exists() :
        return render(request, 'student/dashboard/index.html', {})

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        appl = form.save(commit = False)
        appl.user = request.user
        appl.save()
        return render(request, 'student/dashboard/index.html', {})
    return render(request,'authentication/form.html',{'form' : form})

@login_required
def viewNewApplications(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).filter(placementStatus = 'N')
    listOfEligibleCompanies = []
    for compayApplicaton in company:
        companyName = CompanyApplicants.getCompanyName(compayApplicaton)
        listOfEligibleCompanies.append(companyName)
    print(listOfEligibleCompanies)
    form = ViewCompaniesForm(request.POST or None)
    context = {'eligibleCompanies' : listOfEligibleCompanies, 'form':form}
    if form.is_valid():
        companyName = form.cleaned_data.get('nameOfCompany')
        companyName = companyName.upper()
        for companies in listOfEligibleCompanies:
            if companyName == companies.upper():
                companyName = companies
                break
        if companyName in str(listOfEligibleCompanies):
            companyDetails = Companies.objects.get(name = companyName)
            applicantData = CompanyApplicants.objects.get(student = student, company = companyDetails)
            applicantData.placementStatus = 'A'
            applicantData.save()
            print("Applied")
        else :
            print("You are not eligible for the company")
        return render(request,'student/showCompanies.html',context)
    return render(request,'student/showCompanies.html',context)

@login_required
def viewStatusOfApplication(request):
    user = request.user
    student = Student.objects.get(user = user)
    company = CompanyApplicants.objects.filter(student = student).exclude(placementStatus = 'N').exclude(placementStatus = 'R')
    listOfAppliedCompanies = []
    for compayApplicaton in company:
        companyName = CompanyApplicants.getCompanyName(compayApplicaton)
        listOfAppliedCompanies.append(companyName + " -> " + compayApplicaton.placementStatus)
    print(listOfAppliedCompanies)
    return render(request,'student/showApplied.html',{'eligibleCompanies':listOfAppliedCompanies})

@login_required
def viewProfile(request):
    return render(request,'student/dashboard/pages/profile.html',{})

@login_required
def uploadResume(request):
    form = ResumeForm(request.POST or None)
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
    return render(request,'student/Resume.html',{'form':form})    

@login_required
def showCalendar(request):
    return render(request,'student/dashboard/pages/calendar.html',{})

