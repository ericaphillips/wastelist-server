"""wastelist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from wastelistapi.views import register_user, login_user
from wastelistapi.views import Pharmacies, Users, Profile, Messages   

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'pharmacies', Pharmacies, 'pharmacy')
router.register(r'users', Users, 'user')
router.register(r'profile', Profile, 'profile')
router.register(r'messages', Messages, 'message')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    # (r'^messages/', include('django_messages.urls')),
]
