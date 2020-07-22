from django.conf.urls import url
from . import views

app_name='coordinator'

urlpatterns = [
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
 ]