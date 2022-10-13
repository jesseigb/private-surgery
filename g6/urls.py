from django.urls import path
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin', (admin.site.urls)),
    path('', views.home, name="home"),
    path('homepage', views.home, name="home"),
    path('appointment', views.appointment, name="appointment"),
    path('report', views.report, name="report"),
    path('profile', views.profile, name="profile"),
    path('about', views.about, name="about"),
    path('login', views.login_user, name="login"),
    path('registration', views.registration, name="registration"),
    path('logout_user', views.logout_user, name="logout")
]
