"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from age.views import *
from interest.views import *
from users.views import *
from interestStorage.views import *


urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('about/', AboutPage.as_view(), name='about'),
    path('findAge/', age, name='agepage'),
    path('findInterest/', interest, name='interest'),
    path('storeInterest/', StorageCreateView.as_view(), name='interest-storage'),
    path('listInterests/', storageList, name='list-interests'),
    path('lender/<str:takenperson>/',
         lenderStorageListView, name='lender-interests'),
    path('lender/<int:pk>/delete/', LenderDeleteView.as_view(), name='lender-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('admin/', admin.site.urls)
]
