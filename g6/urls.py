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
    path('doctor/logout', views.logout_doctor, name="logout_doctor"),
    path('doctor/login', views.login_doctor, name="login_doctor"),
    path('doctor/dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('registration', views.registration, name="registration"),
    path('cancel_appointment/<int:id>', views.cancel_appointment, name="cancel_appointment"),
    path('doctor/edit_appointment/<int:id>', views.edit_appointment, name="edit_appointment"),
    path('doctor/add_availability', views.add_availability, name="add_availability"),
    path('doctor/report_reply/<int:id>', views.report_reply, name="report_reply"),
    path('logout_user', views.logout_user, name="logout")
]
