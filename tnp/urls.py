"""tnp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from authentication import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^ccpd', include('authentication.urls', namespace="authentication")),
    url(r'^student/', include('student.urls', namespace="student")),
    url(r'^coordinator/', include('coordinator.urls', namespace="coordinator")),
    url(r'^administrator/', include('administrator.urls', namespace="administrator")),
    url(r'^ccpd/admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^company/', include('company.urls', namespace="company")),
    path('password_reset/',
    auth_views.PasswordResetView.as_view(template_name = 'account/password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
        views.activate_account, name='activate'),
    ]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
