from django.conf.urls import url,include
from . import views

app_name= 'student'

urlpatterns = [
    url(r'^registerStudent',views.registerStudent,name='registerStudent'),
    url(r'^studentDashboard',views.studentDashboard,name='studentDashboard'),
    url(r'^viewNewApplications',views.viewNewApplications,name='viewNewApplications'),
    url(r'^viewStatusOfApplication',views.viewStatusOfApplication,name='viewStatusOfApplication'),
    url(r'^viewProfile',views.viewProfile,name='viewProfile'),
    url(r'^uploadResume',views.uploadResume,name='uploadResume'),
    url(r'^showCalendar',views.showCalendar,name='showCalendar'),
    url(r'^contactTnp',views.contactTnp,name='contactTnp'),
 ]