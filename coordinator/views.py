from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.models import User, Group
from student.models import Student
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CompaniesForm, SearchCompany, UpdatePlacementStatsForm
from .models import Companies
from administrator.models import Branch
from student.models import CompanyApplicants
from .models import Announcement
from .forms import AnnouncementForm, UpdateAnnouncementForm
from company.models import Details
from datetime import datetime, timedelta

# Views
flagDeleted = 0


@login_required
def coordinatorDashboard(request):
    user = request.user
    getAnnouncements = Announcement.objects.filter(
        datePublished__gte=datetime.now() - timedelta(1), datePublished__lte=datetime.now())
    listOfAnnouncements = []
    for announcement in getAnnouncements:
        if announcement.type_of_announcement == 'Broadcasting':
            listOfAnnouncements.append(announcement)
        else:
            companyName = Announcement.getCompanyName(announcement)
            company = Companies.objects.get(name=companyName)
            if CompanyApplicants.objects.filter(student=student).filter(company=company).exists():
                listOfAnnouncements.append(announcement)

    listOfCoordinators = User.objects.filter(groups__name='Coordinator')
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True).filter(groups__name='Coordinator')
    if emails.filter(email=request.user.email).exists():
        context = {'listOfAnnouncements': listOfAnnouncements}
        template = 'coordinator/dashboard/pages/dash.html'
        return render(request, template, context)

    else:
        return HttpResponse("unauthorized")


@login_required
def registerCoordinator(request):
    user = request.user
    listOfCoordinators = User.objects.filter(groups__name='Student')
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True).filter(groups__name='Coordinator')
    if emails.filter(email=request.user.email).exists():
        return HttpResponseRedirect('/coordinator/coordinatorDashboard')

    else:
        return HttpResponse("unauthorized")


@login_required
def addNewCompany(request):
    form = CompaniesForm(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            HttpResponse("The Company name has already been added!")
        else:
            appl = form.save(commit=False)
            appl.user = request.user
            appl.save()
            return HttpResponse("successful")

    context = {'form': form, 'title': 'Add New Company'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def updateCompanyStatus(request):
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        global flagDeleted
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            Companies.objects.get(pk=companyName).delete()
            flagDeleted = 1
        elif flagDeleted == 1:
            form = CompaniesForm(request.POST or None,
                                 initial={'name': companyName})
            if form.is_valid():
                print("hello")
                appl = form.save(commit=False)
                appl.user = request.user
                appl.save()
                return HttpResponse("successful")
        else:
            print("The company was not added before!")

    context = {'form': form, 'title': 'Update Company Status'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def getCompanyStatus(request):
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.filter(name=companyName)
            statusOfCompany = companyDetails.values_list(
                'status', flat=True)[0]
            print(statusOfCompany)
        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'View Company Status'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def sendCompanyDetails(request):
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.filter(name=companyName)
            branchesAllowed = companyDetails.values_list(
                'branchesAllowed', flat=True)[0]
            cgpaAllowed = companyDetails.values_list('CGPA', flat=True)[0]
            listOfBranches = branchesAllowed.split(',')
            for branchElement in listOfBranches:
                branchName = Branch.objects.get(branchCode=branchElement)
                allowedByBranches = Student.objects.filter(
                    branch=branchName).values_list('admissionNumber', flat=True)
                if allowedByBranches.exists():
                    allowedByCGPA = allowedByBranches.filter(
                        CGPA__gte=cgpaAllowed)  # cgpa greater than allowed
                    for allowedStudent in allowedByCGPA:
                        student = Student.objects.get(
                            admissionNumber=allowedStudent)
                        company = Companies.objects.get(name=companyName)
                        newApplicant = CompanyApplicants(
                            company=company, student=student)
                        newApplicant.save()
                    print(allowedByCGPA)
        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'Send Company Details'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def checkApplicantsOfCompany(request):
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.get(name=companyName)
            listOfApplicants = CompanyApplicants.objects.filter(
                placementStatus='A').filter(company=companyDetails)
            print(listOfApplicants)
        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'Check Applicants of Company'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def placedStudents(request):
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.get(name=companyName)
            listOfPlaced = CompanyApplicants.objects.filter(
                placementStatus='P').filter(company=companyDetails)
        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'Placed Students'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def updateStudents(request):
    form = UpdatePlacementStatsForm(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('company')
        status = form.cleaned_data.get('status')
        if Companies.objects.filter(name=companyName).exists():
            students = form.cleaned_data.get('students')
            companyDetails = Companies.objects.get(name=companyName)

            listOfQualifiers = students.split(',')
            for qualifier in listOfQualifiers:
                student = Student.objects.get(rollNumber=qualifier)

                applicantData = CompanyApplicants.objects.get(student=student)
                applicantData.placementStatus = status[0]
                applicantData.save()

        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'Update Students'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def createAnnouncement(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        announcement_id = form.cleaned_data.get('announcementid')
        # text = form.cleaned_data.get('text')
        # company = form.cleaned_data.get('company')
        # datePublished = form.cleaned_data.get('datePublished')
        # typeOfAnnouncement = form.cleaned_data.get('type_of_announcement')
        # companyName = form.cleaned_data.get('company')
        # company = Details.objects.get(name = companyName)
        if Announcement.objects.filter(announcementid=announcement_id).exists():
            HttpResponse("exists")
        else:
            appl = form.save(commit=False)
            appl.user = request.user
            appl.save()
            return redirect('coordinatorDashboard.html')

    context = {'form': form, 'title': 'Create Announcement'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def updateAnnouncement(request):
    form = UpdateAnnouncementForm(request.POST or None)
    if form.is_valid():
        announcement_id = form.cleaned_data.get('announcementid')
        text = form.cleaned_data.get('text')
        typeOfAnnouncement = form.cleaned_data.get('type_of_announcement')
        if Announcement.objects.filter(announcementid=announcement_id).exists():
            # saveDetails = Announcement(announcementid = announcement_id,
            # user = request.user,
            # text = text,
            # type_of_announcement = typeOfAnnouncement
            # )
            # saveDetails.save()
            announce = Announcement.objects.get(announcementid=announcement_id)
            announce.text = text
            announce.save()
            HttpResponse("The announcement was not added before!")

    context = {'form': form, 'title': 'Update Announcement'}
    template = 'authentication/form.html'
    return render(request, template, context)
