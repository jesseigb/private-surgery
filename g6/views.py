from pydoc import Doc
from zoneinfo import available_timezones
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import logging
from django.core.mail import send_mail
from datetime import *
from datetime import datetime
import re

# Create your views here.

from .models import * 
from .forms import CreateUserForm

def home(request):
    return render(request, 'homepage.html', {})

def appointment(request):
    all_availability = Doctor_Availability.objects.all

    if request.method == 'POST':
        
        patient = Patient.objects.get(user=request.user)
        doctor_availability = Doctor_Availability.objects.get(id=request.POST['availability'])
        comment = request.POST['comment']
        
        new_appointment = Appointment(patient=patient,appointment_details=doctor_availability,comment=comment)
        new_appointment.save()
        Doctor_Availability.objects.filter(id=request.POST['availability']).update(full=True)

        messages.success(request, ('Appointment successfully arranged, see you soon!'))

    return render(request, 'appointment.html', {'all': all_availability})

def report(request):
    current_date = date.today().strftime("%Y" + "-" + "%m" + "-" + "%d")
    current_time = datetime.now().strftime("%X")

    if request.method == 'POST':
        patient = Patient.objects.get(user=request.user)
        comment = request.POST['message']

        new_report = Report(patient=patient, personal_doctor=patient.personal_doctor
        ,date=current_date, time=current_time, issue=comment)
        new_report.save()

    return render(request, 'report.html', {})

def registration(request):

    all_doctors = Doctor.objects.all()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            gender = form.cleaned_data['gender']
            date_of_birth = datetime.strptime(request.POST['date_of_birth'], "%Y-%m-%d")
            contact_number = form.cleaned_data['contact_number']
            doctor_id = request.POST['doctor']
            personal_doctor = Doctor.objects.get(id=doctor_id)
            user = authenticate(username=username, password=password)

            new_patient = Patient(user=user,date_of_birth=date_of_birth,gender=gender,contact_number=contact_number,
            personal_doctor=personal_doctor)
            new_patient.save()

            login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form': form, 'doctors': all_doctors}
    return render(request, 'registration.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged off"))
    return redirect('login')

def logout_doctor(request):
    logout(request)
    messages.success(request, ("You were logged off"))
    return redirect('login_doctor')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Credentials do not match"))
            return redirect('login')

    return render(request, 'login.html', {})

def login_doctor(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if Doctor.objects.filter(user=user):
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.success(request, ("Only doctor can have access"))
                return redirect('login_doctor')
        else:
            messages.success(request, ("Credentials do not match"))
            return redirect('login_doctor')

    return render(request, 'doctor_login.html', {})

def profile(request):

    patient = Patient.objects.get(user=request.user)
    all_appointments = Appointment.objects.filter(patient=patient)
    all_reports = Report.objects.filter(patient=patient)

    return render(request, 'my-profile.html', {'appointments': all_appointments, 'patient': patient, 'reports': all_reports})

def doctor_dashboard(request):

    doctor = Doctor.objects.get(user=request.user)
    all_appointments = Appointment.objects.all()
    doctor_appointments = []
    all_reports = Report.objects.filter(personal_doctor=doctor)
    all_availabilities = Doctor_Availability.objects.filter(doctor=doctor, full=False)

    for appointment in all_appointments:
        if appointment.appointment_details.doctor == doctor:
            doctor_appointments.append(appointment)
        
    return render(request, 'doctor-dashboard.html', {'availabilities': all_availabilities,'appointments': doctor_appointments, 'doctor': doctor, 'reports': all_reports})

def about(request):

    doctors = Doctor.objects.all()

    return render(request, 'about-us.html', {'doctors': doctors})

def cancel_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    doctor_availability = Doctor_Availability.objects.filter(id=appointment.appointment_details.id)

    doctor_availability.update(full=False)
    appointment.delete()

    messages.success(request, ('Appointment has been cancelled'))
    return redirect(request.META["HTTP_REFERER"])

def edit_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    doctor_availability = Doctor_Availability.objects.filter(id=appointment.appointment_details.id)
    date = request.GET['date']
    time = request.GET['time']

    doctor_availability.update(date=date, time=time)

    messages.success(request, ('Appointment successfully edited'))
    return redirect('doctor_dashboard')

def add_availability(request):
    doctor = Doctor.objects.get(user=request.user)
    date = request.GET['date']
    time = request.GET['time']

    new_availability = Doctor_Availability(doctor=doctor, date=date, time=time)
    new_availability.save()

    messages.success(request, ('Availability successfully added, get ready!'))
    return redirect('doctor_dashboard')

def report_reply(request, id):
    report = Report.objects.get(id=id)
    patient = report.patient.user
    reply_message = request.GET['reply-text']
    bot_text = ""

    if re.search('suicide|depression|kill my self', report.issue):
        bot_text = 'For mental health concerns please call 116 123, there is always help for you, you are never alone'
    
    email_body = 'Your report: ' + report.issue + "\n" + 'Doctor reply: ' + reply_message + "\n" + bot_text

    report.delete()

    messages.success(request, ('Reply successfully sent'))
    return redirect('doctor_dashboard')