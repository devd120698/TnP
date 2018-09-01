from django.conf.urls import url
from . import views

app_name='administrator'

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^add_company$',views.add_company,name='add_company')
]