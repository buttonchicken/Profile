from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'Accounts'
urlpatterns = [
    path('register',Register.as_view(),name='Register'),
    path('login',Login.as_view(),name='Login'),
    path('update',UpdateProfile.as_view(),name="Update")
] 