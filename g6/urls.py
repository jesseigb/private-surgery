from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('homepage', views.home, name="home"),
    path('appointment', views.appointment, name="appointment"),
    path('report', views.report, name="report"),
    path('registration', views.registration, name="registration"),
    path('profile', views.profile, name="profile"),
    path('login', views.login, name="login"),
]
