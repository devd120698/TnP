from django.conf.urls import url
from . import views

app_name='authentication'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'sign_in$',views.sign_in,name='sign_in'),
    url(r'sign_out$',views.sign_out,name='sign_out'),
 ]