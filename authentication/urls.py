from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='authentication'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    # url(r'sign_in$',views.sign_in,name='log_in'),
    url(r'sign_up$',views.sign_up,name='sign_up'),
    url(r'about_us$',views.about_us,name='about_us'),
    url(r'contact_us$',views.contact_us,name='contact_us'),
    path('login/',auth_views.LoginView.as_view(template_name='authentication/log_in.html'),name='sign_in'),
    path('logout/',auth_views.LogoutView.as_view(template_name='authentication/logout.html'),name='student-logout'),

 ]