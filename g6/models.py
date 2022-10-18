from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This table contains all the registered patients extending
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(max_length=200)
    gender = models.CharField(max_length=200, choices=[('Male','Male'), ('Female', 'Female')])
    contact_number = models.IntegerField
    personal_doctor = models.ForeignKey (
        'Doctor',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

# This table containes all the doctors 
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)

# This table handles all the appoinments that have been fixed
class Appointment(models.Model):
    patient = models.ForeignKey (
        'Patient',
        on_delete=models.CASCADE,
    )
    appointment_details = models.ForeignKey (
        'Doctor_Availability',
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=200, blank=True, null=True)

# This a list of all doctor availabilities where patient can choose 
# from to book an appoinment
class Doctor_Availability(models.Model):
    doctor = models.ForeignKey (
        'Doctor',
        on_delete=models.CASCADE,
    )
    date = models.DateField(max_length=200)
    time = models.TimeField(max_length=200)
    full = models.BooleanField(default=False)

# This table handles all the reports made by patients
class Report(models.Model):
    patient = models.ForeignKey (
        'Patient',
        on_delete=models.CASCADE,
    )
    personal_doctor = models.ForeignKey (
        'Doctor',
        on_delete=models.CASCADE,
    )
    date = models.DateField(max_length=200)
    time = models.TimeField(max_length=200)
    issue = models.CharField(max_length=200)
