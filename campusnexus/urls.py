"""
URL configuration for campusnexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from users.views import *
from clubadmins.views import *
from events.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/userhome/', Clubslist.as_view(), name = "usershome"),
    path('api/v1/userhome/login', StudentLogin.as_view(), name="StudentLogin"),
    path('api/v1/adminhome/register', ClubAdminsRegister.as_view(), name="Clubadminregister"),
    path('api/v1/userhome/events/', Eventslist.as_view(), name = "eventslist"),
    path('api/v1/userhome/<str:clubid>/events', Clubevents.as_view(), name="clubevents"),
    path('api/v1/userhome/<str:clubid>/events/<str:eventid>', Eventsdetails.as_view(), name="clubevents"),
    path('api/v1/userhome/<str:clubid>/about', Clubinfo.as_view(), name="clubinfo"),
    path('api/v1/userhome/<str:clubid>/events/<str:eventid>/register', StRegValidation.as_view(), name="StRegValidation"),
    path('api/v1/userhome/<str:strollno>/myregistrations', Stregistrations.as_view(), name="Stregistrations"),
    path('api/v1/userhome/register', StudentRegistration.as_view(), name="StudentRegistration"),
    path('api/v1/adminhome/login', ClubAdminLogin.as_view(), name="Clubadminlogin"),
    path('api/v1/adminhome/<str:clubid>', Clubinfo.as_view(), name="Adminhome"),
    path('api/v1/adminhome/<str:clubid>/events', Clubevents.as_view(), name="Adminclubevents"),
    path('api/v1/adminhome/<str:clubid>/registerevent',AdminEventRegistration.as_view(),name="Admineventregistration"),
    path('api/v1/adminhome/<str:clubid>/editevent/<str:eventid>',AdminEditEvent.as_view(),name="Admineditevent")
]
