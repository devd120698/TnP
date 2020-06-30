from django.conf.urls import url,include
from . import views

app_name= 'student'

urlpatterns = [
    url(r'^registerStudent',views.registerStudent,name='registerStudent'),
    url(r'^studentDashboard',views.studentDashboard,name='studentDashboard'),
 ]