from pydoc import Doc
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import logging
from django.core.mail import send_mail
from datetime import *

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

        # Send an email
        send_mail(
            'Appointment Confirmation', # Email Subject
            'On the ' + str(new_appointment.appointment_details.date) + ' at ' 
            + str(new_appointment.appointment_details.time) + ' with Dr. ' 
            + new_appointment.appointment_details.doctor.user.first_name + ' ' + new_appointment.appointment_details.doctor.user.last_name, # Email body message
            '1yunusarslan1@gmail.com', # From email
            [request.user.email], # To email
        )


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
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'registration.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged off"))
    return redirect('login')

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

#------- Doctors Login -------#
def login_doctor(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if Doctor.objects.filter(user=user):
                login(request, user)
                return redirect('home')
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
    all_appointments = Appointment.objects.filter(patient=patient)
    all_reports = Report.objects.filter(personal_doctor=doctor)

    return render(request, 'doctor-dashboard.html', {'appointments': all_appointments, 'doctor': doctor, 'reports': all_reports})

def about(request):
    return render(request, 'about-us.html', {})


