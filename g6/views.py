from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import logging

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

    return render(request, 'appointment.html', {'all': all_availability})

def report(request):
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

def profile(request):

    patient = Patient.objects.get(user=request.user)
    all_appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'my-profile.html', {'appointments': all_appointments, 'patient': patient})

def about(request):
    return render(request, 'about-us.html', {})


