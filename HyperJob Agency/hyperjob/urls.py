"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.shortcuts import render


# it is defined here cause it is a central handler(does not belong to other apps)
# and I did not want to create a separate file for a function
def menu(request):
    menu_links = ['login', 'signup', 'vacancies', 'resumes', 'home']
    return render(request, 'base/menu.html', context={'links': menu_links})


def home(request):
    return render(request, 'base/home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu, name='menu'),
    path('home', home, name='home'),
    path('vacancies', include('vacancy.urls')),
    path('resumes', include('resume.urls')),
    path('', include('users.urls')),
]
