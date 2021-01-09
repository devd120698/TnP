from __future__ import unicode_literals
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import *
from .models import Student
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect , StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from coordinator.models import *
from administrator.models import Branch
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib import messages
import sys
import csv
import pandas as pd
import dask.dataframe as dd

noOfAnnouncements = 0
student  = None

def get_student_details(user_id):
    student_user = StudentUser.objects.get(id = user_id)
    resume_oject = Resume.objects.get(user = student_user)
    
    print(student_user)
    student_data = StudentData.objects.get(userid = user_id)
    name = student_data.name
    reg_number = student_data.registration_number
    student_mail_details = MailAll.objects.get(registration_number=reg_number)
    branch = student_data.branch
    year_of_graduation = (student_data.joining_year) 
    roll_number = student_data.roll_number
    cgpa = resume_oject.CGPA
    resume_url = resume_oject.resume
    address = student_data.address
    mob_number = student_data.mobile
    course = student_data.course
    email = student_user.email
    twelth_perc = resume_oject.twelth_perc
    tenth_perc = resume_oject.tenth_perc
    student = {
        'user_id' : user_id,
        'name' : name ,
        'admissionNumber' : reg_number,
        'branch' : branch,
        'course' : course,
        'yearOfGraduation' : year_of_graduation,
        'rollNumber' : roll_number,
        'CGPA' : cgpa,
        'address' : address,
        'mobileNumber' : mob_number,
        'profile_image' : student_data.profile_image,
        'resume_url' : resume_url,
        'email' :email,
        'student_email' : student_mail_details.email_id,
        'twelth_perc' : twelth_perc,
        'tenth_perc' : tenth_perc,
        'company_placed' : ''
        
    }
    # print(student)
    return student

@login_required
def studentDashboard(request):
    global noOfAnnouncements
    print(request.user)
    print(request.user.id)
    print("hi")
    student_user = StudentUser.objects.get(id = request.user.id)
    print(len(Resume.objects.filter(user=student_user)))
    if(not len(Resume.objects.filter(user=student_user))):
        return redirect('/ccpd/student/addCGPA')
       
    getAnnouncements = Announcement.objects.filter(datePublished__gte = datetime.now() - timedelta(1), datePublished__lte = datetime.now())
    student = get_student_details(request.user.id)
    listOfAnnouncements = []
    for announcement in getAnnouncements:
        if announcement.type_of_announcement == 'Broadcasting':
            listOfAnnouncements.append(announcement)
        else:
            company = Announcement.getCompanyName(announcement)
            
            if CompanyApplicants.objects.filter(student = request.user).filter(company = company).exists():
                listOfAnnouncements.append(announcement)
        
        global noOfAnnouncements
        noOfAnnouncements = len(listOfAnnouncements)
        
    # student = Student.objects.get(user = request.user)

    
    return render(request, 'student/dashboard/pages/dashboard.html', {'student':student,'noOfAnnouncements': noOfAnnouncements, 'listOfAnnouncements':listOfAnnouncements  })

@login_required
def registerStudent(request):
    user = request.user
    branches = Branch.objects.all()
    if Student.objects.filter(user = user).exists() :
        
        return HttpResponseRedirect('/ccpd/student/studentDashboard')

    rollNumber = request.POST.get('rollNumber')

    if rollNumber != None:
        if Student.objects.filter(rollNumber = rollNumber).exists():
            return HttpResponse("already registered")
        
        else:
            branchName = request.POST.get('branches')
            saveDetails = Student(
                name = request.POST.get('name'),
                user = request.user,
                admissionNumber = request.POST.get('admNumber'),
                rollNumber = rollNumber,
                branch = Branch.objects.get(branch = branchName),
                yearOfGraduation = request.POST.get('yearOfGraduation'),
                CGPA = request.POST.get('CGPA'),
                address = request.POST.get('address'),
                mobileNumber = request.POST.get('mobNo')
            )
            saveDetails.save()
            return HttpResponseRedirect('studentDashboard')
    return render(request,'Register/studentRegister.html',{'branches':branches})

@login_required
def viewNewApplications(request):
    student_user = StudentUser.objects.get(id = request.user.id)
    print(len(Resume.objects.filter(user=student_user)))
    if(not len(Resume.objects.filter(user=student_user))):
        return redirect('/ccpd/student/addCGPA')
    if request.method == 'GET':
        student = get_student_details(request.user.id)
        all_companies = Companies.objects.filter(CGPA__lte = student['CGPA'] , existing_status='Alive')
        print(all_companies)
        final_companies= []
        for company in all_companies:
            branches = company.branchesAllowed
            
            if(branches == None ):
                continue 
            listOfBranches = branches.split(',')
            resume_object = Resume.objects.get(user= request.user)
            if resume_object.branch in listOfBranches:
                final_companies.append(company)


        ## check eligibility
        context = {'eligibleCompanies' : final_companies ,'student' : student}
        return render(request,'student/showCompanies.html',context)
    if request.method == 'POST': 
        student = get_student_details(request.user.id)

        user = request.user
        company = CompanyApplicants.objects.filter(student = user).filter(placementStatus = 'N')
        print(company)
        context = {'eligibleCompanies' : company, 'student':student}
        companyName = request.POST.get('nameOfCompany')
        print(companyName, "hello")
        
        if companyName != None :
            companyDetails = Companies.objects.get(name = companyName)
            context = {'company_details' : companyDetails , 'student' : student , }
            return render(request , 'student/company_application_form.html' , context)
            
            
        return render(request,'student/showCompanies.html',context)

@login_required
def applyForCompany(request):
    student_user = StudentUser.objects.get(id = request.user.id)
    print(len(Resume.objects.filter(user=student_user)))
    if(not len(Resume.objects.filter(user=student_user))):
        return redirect('/ccpd/student/addCGPA')
    companyName = request.POST.get('company')
    student_id = request.POST.get('student_id')
    print(companyName)
    print(student_id)
    student_user = StudentUser.objects.get(id=student_id)
    student = get_student_details(student_id)
    if CompanyApplicants.objects.filter(company=companyName).filter(student=student_user).exists():
        messages.error(request , "You have already Applied for this Company")
        companyDetails = Companies.objects.get(name = companyName)
        context = {'company_details' : companyDetails , 'student' : student , }
        return render(request , 'student/company_application_form.html' , context)
    else: 
        companyDetails = Companies.objects.get(name = companyName)
        applicantData = CompanyApplicants()
        applicantData.student = StudentUser.objects.get(id=student_id)
        applicantData.company = companyDetails
        applicantData.placementStatus = 'A'
        applicantData.save()

        text_to_be_sent = 'Dear ' + student['name'] + ',\n' + 'You have successfully applied to be a part of the placement drive for the company - ' +  companyName + '. We will be reaching out to you with further notifications about the process.\n' + 'Best Regards\n' + 'CCPD.'
        send_mail(
            'Application Confirmation',
            text_to_be_sent,
            'taps@nitw.ac.in',
            [request.user.email],
            fail_silently=True,
        )
        
        return redirect('/ccpd/student/viewNewApplications')
# login_required
def viewStatusOfApplication(request):
    student_user = StudentUser.objects.get(id = request.user.id)
    print(len(Resume.objects.filter(user=student_user)))
    if(not len(Resume.objects.filter(user=student_user))):
        return redirect('/ccpd/student/addCGPA')
    student = get_student_details(request.user.id)
    user = request.user
    company = CompanyApplicants.objects.filter(student = user).exclude(placementStatus = 'N').exclude(placementStatus = 'R')
    return render(request,'student/showApplied.html',{'eligibleCompanies':company, 'student':student})

@login_required
def viewProfile(request):
    student_user = StudentUser.objects.get(id = request.user.id)
    print(len(Resume.objects.filter(user=student_user)))
    if(not len(Resume.objects.filter(user=student_user))):
        return redirect('/ccpd/student/addCGPA')
    student = get_student_details(request.user.id)

    resumeUploaded = False
    resume_url = ""
    if Resume.objects.filter(user = request.user).exists():
        resumeUploaded = True
        resume_url = Resume.objects.get(user=request.user).resume
    
    return render(request,'student/dashboard/pages/profile.html',{'student':student, 'resumeUploaded': resumeUploaded, 'resume_url' :resume_url })

@login_required
def uploadResume(request):
    # student = Student.objects.get(user = request.user)
    # print(request.POST.get('educationAll'))

    # if request.POST.get('educationAll') != None:
    #     education = request.POST.get('educationAll')
    #     projectAll = request.POST.get('projectAll')
    #     acheievementsAll = request.POST.get('acheievementsAll')
    #     relevantCoursesAll = request.POST.get('relevantCoursesAll')
    #     skillsAll = request.POST.get('skillsAll')
    #     extraCurricularAll = request.POST.get('extraCurricularAll')

    #     saveDetails = Resume(
    #         name = request.POST.get('name'),
    #         year = request.POST.get('year'),
    #         email = request.POST.get('email'),
    #         phoneNumber = request.POST.get('phone'),
    #         address = request.POST.get('address'),
    #         student = student,
    #         education = education,
    #         projects = projectAll,
    #         achievements = acheievementsAll,
    #         skills = skillsAll,
    #         relevantCourses = relevantCoursesAll,
    #         extraCurricular = extraCurricularAll
    #     )

    #     print(saveDetails)
    #     saveDetails.save()
    # return render(request,'student/dashboard/pages/resume-form.html',{'student':student})   
    if(request.method == 'POST'):
        try :

            student = get_student_details(request.user.id)
            resume_url  = request.POST.get('resume' , False)
            print(resume_url)
            if(Resume.objects.filter(user = request.user).exists()):
                req_resume =Resume.objects.get(user=request.user)
                req_resume.resume = resume_url
                req_resume.save()
            else :
                saveResume = Resume(
                    user=request.user ,
                    resume=resume_url
                )
                saveResume.save()
            
            
            messages.success(request , "Resume URL Updated Successfully")
            return render(request,'student/dashboard/pages/resume.html')
            
        except :
            print("Unexpected error:", sys.exc_info()[0])
            messages.error(request , "Could Not Update Your Resume URL")
            return render(request,'student/dashboard/pages/resume.html')
    else :
        return render(request,'student/dashboard/pages/resume.html')
        
@login_required
def addCGPA(request):
    if(request.method=='POST'):
        cgpa = request.POST.get('CGPA', False)
        twelth_perc = request.POST.get('twelth_perc', False)
        tenth_perc = request.POST.get('tenth_perc', False)
        branch = request.POST.get('branches' , False)
        resume_url  = request.POST.get('resume' , False)
        if(Resume.objects.filter(user = request.user).exists()):
            req_resume =Resume.objects.get(user=request.user)
            req_resume.resume = resume_url
            req_resume.CGPA=cgpa
            req_resume.twelth_perc=twelth_perc
            req_resume.branch = branch
            req_resume.tenth_perc = tenth_perc
            req_resume.save()
        else :
            
            saveResume = Resume(
                        user=request.user ,
                        resume=resume_url,
                        tenth_perc=tenth_perc,
                        twelth_perc=twelth_perc,
                        CGPA=cgpa,
                        branch=branch

                    )
            
            saveResume.save()
        messages.success(request , "Details Updated Successfully")
        return redirect('/ccpd/student/studentDashboard')
    else : 
        return render(request,'student/dashboard/pages/addCgpa.html')

# @login_required
def showCalendar(request):
    #student = Student.objects.get(user = request.user)
    student = 'abcd'
    return render(request,'student/dashboard/pages/calendar.html',{'student':student})


@login_required
def contactTnp(request):
    student = get_student_details(request.user.id)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        mailid = form.cleaned_data.get('mailid')
        message = form.cleaned_data.get('message')
        saveDetails = Contact(
            name = name,
            mailid = mailid,
            message = message
        )
        saveDetails.save()
        send_mail(
		    name + ' contacting CCPD',
		    message,
		    'taps@nitw.ac.in',
		    [mailid],
		    fail_silently=True,
	    )
		
    return render(request,'student/Resume.html',{'form':form, 'student':student})  

###### Views related to coo-rdinator ###### 
def check_coordinator(user):
    curr_user_details = get_student_details(user.id)
    return  len(Coordinator.objects.filter(registration_number=curr_user_details['admissionNumber'])) > 0

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
            company = Announcement.getCompanyName(announcement)
            
            if CompanyApplicants.objects.filter(student=student).filter(company=company).exists():
                listOfAnnouncements.append(announcement)

    listOfCoordinators = Coordinator.objects.all()
    print(listOfCoordinators)
    curr_user_details = get_student_details(request.user.id)
    check  = Coordinator.objects.filter(registration_number=curr_user_details['admissionNumber'])
    print(check)
    if(check_coordinator(request.user)):
        context = {'listOfAnnouncements': listOfAnnouncements , 'curr_user' : curr_user_details}
        template = 'coordinator/dashboard/pages/dash.html'
    
        return render(request, template, context)
    else:

        return HttpResponse("unauthorized")
    




@login_required
def registerCoordinator(request):
    listOfCoordinators = Coordinator.objects.all()
    curr_user_details = get_student_details(request.user.id)
    check  = Coordinator.objects.filter(registration_number=curr_user_details['admissionNumber'])
    emails = User.objects.filter(is_active=True).values_list(
        'email', flat=True).filter(groups__name='Coordinator')
    if emails.filter(email=request.user.email).exists():
        return HttpResponseRedirect('/ccpd/coordinator/coordinatorDashboard')

    else:
        return HttpResponse("unauthorized")


@login_required
def addNewCompany(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    instance = None
    context = {}
    if request.POST:
        try:
            name = request.POST.get('name')
            instance = Companies.objects.get(name=name)
        except Companies.DoesNotExist:
            pass
    form = CompaniesForm(request.POST or None , instance = instance)
    branches = Branch.objects.all()
    options_html = ""
    for b in branches :
        options_html += '<option value="'+b.branch+'">'+b.branch+'</option>'
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        
        appl = form.save(commit=False)
        appl.user = request.user
        appl.save()
        print("save")
        #return HttpResponse("successful")
        return HttpResponseRedirect('/ccpd/student/coordinatorDashboard')

    context = {'form': form, 'title': 'Add/Update New Company' ,'options_html' : options_html}
    template = 'authentication/add_company_form.html'
    print("here")
    return render(request, template, context)


@login_required
def deleteCompany(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            company_object = Companies.objects.get(name=companyName)
            company_object.existing_status = 'Dead'
            company_object.save()
            messages.success(request,"The company is deleted")
        else:
            #print("The company was not added before!")
            messages.error(request,"The company was not added before!")

    context = {'form': form, 'title': 'Update Company Status'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def getCompanyStatus(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.filter(name=companyName)
            statusOfCompany = companyDetails.values_list(
                'status', flat=True)[0]
            #print(statusOfCompany)
            #return HttpResponse(statusOfCompany)
            messages.info(request, statusOfCompany)
        else:
            #return HttpResponse("The company was not added before!")
            messages.error(request,"The company was not added before!")
            

    context = {'form': form, 'title': 'View Company Status'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def sendCompanyDetails(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
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
                    #print(allowedByCGPA)
                    return HttpResponse(allowedByCGPA)
        else:
            #return HttpResponse("The company was not added before!")
            messages.error(request,"The company was not added before!")

    context = {'form': form, 'title': 'Send Company Details'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def checkApplicantsOfCompany(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")

    form = SearchCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        print(companyName)
        if Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.get(name=companyName)
            listOfApplicants = CompanyApplicants.objects.filter(
                placementStatus='A').filter(company=companyDetails)
            detailsOfApplicants = []
            for student in listOfApplicants:
                
                studentDetails = get_student_details(student.student_id)
                detailsOfApplicants.append(studentDetails)
                
            print(detailsOfApplicants)
            #messages.info(request,listOfApplicants)
            context ={'applicants' : detailsOfApplicants , 'company_name' : companyName}
            template = 'coordinator/viewCompanyApplicants.html'
            return render(request, template, context)
        else:
            #return HttpResponse("The company was not added before!")
            messages.error(request,"The company was not added before!")

    context = {'form': form, 'title': 'Check Applicants of Company'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def placedStudents(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    form = PlacedCompany(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('name')
        
        if companyName == 'All Companies':
            listOfPlaced = CompanyApplicants.objects.filter(
                placementStatus='P')

            detailsOfApplicants = []
            for student in listOfPlaced: 
                studentDetails = get_student_details(student.student_id)
                placed_applicants = CompanyApplicants.objects.filter(student=StudentUser.objects.get(id=student.student_id) , placementStatus='P')
                for s in placed_applicants :
                    studentDetails['company_placed']+=' , '+s.company.name
    
                detailsOfApplicants.append(studentDetails)
                context ={'applicants' : detailsOfApplicants }
                template = 'coordinator/viewAllCompanyApplicants.html'
                return render(request, template, context)
        elif Companies.objects.filter(name=companyName).exists():
            companyDetails = Companies.objects.get(name=companyName)
            listOfPlaced = CompanyApplicants.objects.filter(
                placementStatus='P').filter(company=companyDetails)
            detailsOfApplicants = []
            for student in listOfPlaced:
                
                studentDetails = get_student_details(student.student_id)
                detailsOfApplicants.append(studentDetails)
                
           
            #messages.info(request,listOfApplicants)
            context ={'applicants' : detailsOfApplicants , 'company_name' : companyName}
            template = 'coordinator/viewCompanyApplicants.html'
            return render(request, template, context)
        else:
            HttpResponse("The company was not added before!")

    context = {'form': form, 'title': 'Placed Students'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def updateStudents(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    form = UpdatePlacementStatsForm(request.POST or None)
    if form.is_valid():
        companyName = form.cleaned_data.get('company')
        print(companyName)
        status = form.cleaned_data.get('status')
        try :
        
            student_roll_number = form.cleaned_data.get('student_roll')
            companyDetails = Companies.objects.get(name=companyName)
            print(student_roll_number)
            student_id = StudentData.objects.get(roll_number=student_roll_number).userid
            print(student_id)
            applicantData = CompanyApplicants.objects.filter(student_id=student_id).get(company = companyName)
            applicantData.placementStatus = status[0]
            applicantData.save()
            messages.success(request , 'successfully updated')
            
            
        except :
           messages.error(request , 'student did not apply for the company')

    context = {'form': form, 'title': 'Update Students' }
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def createAnnouncement(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
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
            appl.user = request.user.id
            appl.save()
            return redirect('coordinatorDashboard.html')

    context = {'form': form, 'title': 'Create Announcement'}
    template = 'authentication/form.html'
    return render(request, template, context)


@login_required
def updateAnnouncement(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
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
    return render(request,template,context)

@login_required
def allCompanies(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    companies = Companies.objects.all()
    companyName = ''
    if request.method == 'POST':
        companyName = request.POST.get("companyName")
        companies = Companies.objects.filter(name__istartswith = companyName)
    record = {}
    for company in companies:
        status = company.status
        applicants = CompanyApplicants.objects.filter(company = company)
        record[company] = {'status' : status}
    template = 'coordinator/dashboard/pages/allCompanies.html'
    return render(request,template,{'record' : record, 'value' : companyName})

@login_required
def companyApplicants(request,companyId):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    print(companyId)
    company = Companies.objects.filter(companyID = companyId).first()
    status = company.status
    applicants = CompanyApplicants.objects.filter(company = company)
    students = []
    if(status == 'Accepted'):
        for applicant in applicants:
            if applicant.placementStatus == 'P':
                students.append({'student' : applicant.student, 'placementStatus' :applicant.placementStatus})
    else:
        for applicant in applicants:
            if applicant.placementStatus != 'P':
                students.append({'student' : applicant.student, 'placementStatus' :applicant.placementStatus})
    template = 'coordinator/dashboard/pages/companyApplicants.html'
    return render(request,template,{'company':company, 'students' : students})


@login_required
def searchStudent(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    context = {}
    template = 'coordinator/dashboard/pages/searchStudents.html'
    if request.method == 'POST':
        rollNumber = request.POST.get("rollNumber")
        student = Student.objects.filter(rollNumber = rollNumber).first()
        print(student)
        applications = CompanyApplicants.objects.filter(student = student)
        applied = []
        for app in applications:
            applied.append({'company' : app.company, 'status' : app.placementStatus})

        print(applied)
        context['student'] = student
        context['applications'] = applied
        context['value'] = rollNumber
        return render(request,template, context)
    return render(request, template, context)


@login_required
def viewCompanyDetails(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    companies = Details.objects.all()
    print(companies)
    return render(request , 'coordinator/viewCompanyDetails.html' , {'dict':companies})


@login_required
def merge2csv(request):
    if ( not check_coordinator(request.user)):
        return HttpResponse("unauthorized")
    if(request.method == "POST"):
        df1 =  pd.read_csv(request.FILES['file1'].temporary_file_path())
        df2 =  pd.read_csv(request.FILES['file2'].temporary_file_path())
        
        df3 = pd.merge(df1, df2, on = 'Email')
        merged_file= df3.to_html().replace('<table','<table class="table" id="merged"')
        print(merged_file   )
        return render(request , 'coordinator/dashboard/mergedCsv.html', {'merged_file' : merged_file})
        return HttpResponse(merged_file)
        print(df3)
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="merged_file.csv"'
        # csv_writer = csv.DictWriter(
        #     response,

        #     extrasaction='ignore'
        # )
        # csv_writer.writeheader()
        # total_rows=len(df3.axes[0])

        # for i in range(0,total_rows):
        #     print(df3.loc[[i]])
        #     csv_writer.writerow(df3.loc[[i]])

    
        # return response

        # print(df3)
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="csv_database_write.csv"'
        # return render(request , 'coordinator/merge2csv.html' , {'converted_file' : df3})
    return render(request , 'coordinator/merge2csv.html' )