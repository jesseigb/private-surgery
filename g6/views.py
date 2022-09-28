from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'homepage.html', {})

def appointment(request):
    return render(request, 'appointment.html', {})

def report(request):
    return render(request, 'report.html', {})

def registration(request):
    return render(request, 'registration.html', {})

def login(request):
    return render(request, 'login.html', {})

def profile(request):
    return render(request, 'my-profile.html', {})