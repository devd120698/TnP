from django.conf.urls import url
from . import views

app_name='company'

urlpatterns = [
    url(r'^companyForm',views.companyForm,name='companyForm'),
    url(r'^updateCompanyForm',views.updateCompanyForm,name='updateCompanyForm'),
    url(r'^companyDashboard',views.companyDashboard,name='companyDashboard'),
    url(r'^uploadLoginDetails',views.uploadLoginDetails,name='uploadLoginDetails'),
    url(r'^uploadSchedule',views.uploadSchedule,name='uploadSchedule'),
    url(r'^selectedStudents',views.selectedStudents,name='selectedStudents'),
    url(r'^linkForTest',views.linkForTest,name='linkForTest'),
    url(r'^viewApplicants',views.viewApplicants,name='viewApplicants'),
    url(r'^contact/$', views.contacTnp, name='contact'),
 ]