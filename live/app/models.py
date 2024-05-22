from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    bystander = models.CharField(max_length=100)
    bystandercontact = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    bp = models.CharField(max_length=20, null=True, blank=True)
    sugar = models.CharField(max_length=20, null=True, blank=True)
    cntry=models.CharField(max_length=100)
    image = models.ImageField(upload_to='patimage', null=True, blank=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    # verification_code = models.CharField(max_length=100, blank=True, null=True)
    last_login=models.DateTimeField(null=True,blank=True)
    # otp = models.CharField(max_length=6, blank=True, null=True)  # Add OTP field
   


class DoctorRegister(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    exp=models.CharField(max_length=100)
    spec=models.CharField(max_length=100)
    cntry=models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    image = models.ImageField(upload_to='docimage', null=True, blank=True)
    desc = models.TextField()
    is_active = models.BooleanField(default=False)
    # verification_code = models.CharField(max_length=100, blank=True, null=True)
    last_login=models.DateTimeField(null=True,blank=True)



class MedicalRecord(models.Model):
    patient_name = models.CharField(max_length=100)
    medicine = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField()
    allergies = models.TextField()

    def __str__(self):
        return self.patient_name