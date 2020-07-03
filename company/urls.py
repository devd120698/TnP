from django.conf.urls import url
from . import views

app_name='company'

urlpatterns = [
    url(r'^companyForm',views.companyForm,name='companyForm'),
    
 ]