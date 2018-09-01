from django.conf.urls import url
from . import views

app_name='coordinator'

urlpatterns = [
    url(r'^$',views.index,name='index'),
 ]