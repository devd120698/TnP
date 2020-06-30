from django.conf.urls import url,include
from . import views

app_name= 'student'

urlpatterns = [
<<<<<<< HEAD
    url(r'^registerStudent',views.registerStudent,name='registerStudent'),
    url(r'^studentDashboard',views.studentDashboard,name='studentDashboard'),
=======
    url(r'registerStudent$',views.registerStudent,name='registerStudent'),
    url(r'studentDashboard$',views.studentDashboard,name='studentDashboard'),
>>>>>>> master
 ]