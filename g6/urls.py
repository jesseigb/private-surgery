from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('homepage', views.home, name="home"),
    path('appointment', views.appointment, name="appointment"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
]
