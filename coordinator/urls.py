from django.conf.urls import url
from . import views

app_name='coordinator'

urlpatterns = [
    url(r'^registerCoordinator',views.registerCoordinator,name='registerCoordinator'),
    url(r'^coordinatorDashboard',views.coordinatorDashboard,name='coordinatorDashboard'),
 ]