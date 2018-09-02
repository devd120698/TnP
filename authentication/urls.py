from django.conf.urls import url
from . import views

app_name='authentication'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'sign_in$',views.sign_in,name='sign_in'),
    url(r'sign_out$',views.sign_out,name='sign_out'),
    url(r'log_in$',views.log_in,name='log_in'),
    url(r'about_us$',views.about_us,name='about_us'),
    url(r'contact_us$',views.contact_us,name='contact_us'),
    url(r'sign_up$',views.sign_up,name='sign_up'),
 ]