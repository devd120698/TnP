from django.conf.urls import url,include
from django.urls import path
from . import views

app_name= 'student'

urlpatterns = [
    url(r'^registerStudent',views.registerStudent,name='registerStudent'),
    url(r'^studentDashboard',views.studentDashboard,name='studentDashboard'),
    url(r'^viewNewApplications',views.viewNewApplications,name='viewNewApplications'),
    url(r'^viewStatusOfApplication',views.viewStatusOfApplication,name='viewStatusOfApplication'),
    url(r'^viewProfile',views.viewProfile,name='viewProfile'),
    url(r'^uploadResume',views.uploadResume,name='uploadResume'),
    url(r'^addCGPA',views.addCGPA,name='addCGPA'),
    url(r'^showCalendar',views.showCalendar,name='showCalendar'),
    url(r'^contactTnp',views.contactTnp,name='contactTnp'),


    ##### coordinator urls #####

    url(r'^registerCoordinator',views.registerCoordinator,name='registerCoordinator'),
    url(r'^coordinatorDashboard',views.coordinatorDashboard,name='coordinatorDashboard'),
    url(r'^addNewComapny',views.addNewCompany,name='addNewCompany'),
    url(r'^updateCompanyStatus',views.updateCompanyStatus,name='updateCompanyStatus'),
    url(r'^getCompanyStatus',views.getCompanyStatus,name='getCompanyStatus'),
    url(r'^sendCompanyDetails',views.sendCompanyDetails,name='sendCompanyDetails'),
    url(r'^checkApplicantsOfCompany',views.checkApplicantsOfCompany,name='checkApplicantsOfCompany'),
    url(r'^placedStudents',views.placedStudents,name='placedStudents'),
    url(r'^updateStudents',views.updateStudents,name='updateStudents'),
    url(r'^updateAnnouncements',views.updateAnnouncement,name='updateAnnouncements'),
    url(r'^createAnnouncements',views.createAnnouncement,name='createAnnouncements'),
    url(r'^allCompanies', views.allCompanies, name='allCompanies'),
    url(r'^searchStudent', views.searchStudent, name = 'searchStudent'),
    url(r'^viewCompanyDetails', views.viewCompanyDetails, name = 'viewCompanyDetails'),
    url(r'^applyForCompany', views.applyForCompany, name = 'applyForCompany'),
    path('companyApplicants/<slug:companyId>', views.companyApplicants, name = 'companyApplicants'),
 ]