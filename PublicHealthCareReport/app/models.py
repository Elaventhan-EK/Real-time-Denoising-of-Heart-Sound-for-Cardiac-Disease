from django.conf import settings
from django.db import models
from django.utils import timezone
import random

def create_new_ref_number():
      return str(random.randint(10000, 99999))
COLOR_CHOICES = (
	('','Select'),
    ('govt','Govt Doctor'),
    ('pvt', 'Private Doctor'),)
class Doctor_Detail(models.Model):
    doctor_name = models.CharField(max_length=30,null=True)
    email = models.EmailField(max_length=30,null=True)
    phone_number = models.CharField(max_length=30,null=True)
    doc_license_no = models.CharField(max_length=30,unique=True,null=True)
    hospital_license_no = models.CharField(max_length=30,unique=True,null=True)
    doc_license_expire_date = models.DateField(max_length=30,null=True)
    hospital_license_expire_date = models.DateField(max_length=30,null=True)
    country = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=30,null=True)
    city = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=200,null=True)
    hospital_address = models.CharField(max_length=200,null=True)
    doctor_type = models.CharField(max_length=20, choices=COLOR_CHOICES, default='',null=True)
    def __str__(self):
    	return self.doctor_name
class Doctor_Register(models.Model):
	hospital_name = models.CharField(max_length=40,unique=True)
	doctor_name = models.CharField(max_length=30)
	mail = models.EmailField(max_length=30)
	mobile = models.CharField(max_length=15)
	doc_license_no = models.CharField(max_length=30,unique=True)
	hospital_license_no = models.CharField(max_length=30,unique=True)
	degree = models.CharField(max_length=30,null=True)
	specialist = models.CharField(max_length=30,null=True)
	username = models.CharField(max_length=40,unique=True)
	password = models.CharField(max_length=40)
	country = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	hospital_address = models.CharField(max_length=200)
	doctor_type = models.CharField(max_length=20, choices=COLOR_CHOICES, default='',null=True)
	def __str__(self):
		return self.doctor_name
class Visiting_Detail(models.Model):
	hospital_id =  models.ForeignKey(Doctor_Register, on_delete=models.CASCADE)
	visiting_hour_weekdays = models.CharField(max_length=30)
	visiting_hour_weekend = models.CharField(max_length=30)
	visiting_hour_online_weekdays = models.CharField(max_length=30)
	visiting_hour_online_weekend = models.CharField(max_length=30)
	def __str__(self):
		return self.visiting_hour_weekdays
class Customer_Detail(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	phone_number = models.CharField(max_length=30)
	country =  models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	username = models.CharField(max_length=30,unique=True)
	password =  models.CharField(max_length=30)
	def __str__(self):
		return self.name
class Appointment(models.Model):
	hospital_id =  models.ForeignKey(Doctor_Register, on_delete=models.CASCADE)
	customer_id =  models.ForeignKey(Customer_Detail, on_delete=models.CASCADE)
	pet_name = models.CharField(max_length=30)
	problem =  models.CharField(max_length=200)
	visiting_date = models.DateField(max_length=30)
	visiting_time = models.CharField(max_length=30)
	status = models.CharField(max_length=30)
	def __str__(self):
		return self.customer_id.name
class Patient_Detail(models.Model):
	patient_id =  models.CharField(max_length = 10,blank=True,editable=False,unique=True,default=create_new_ref_number())
	patient_name =  models.ForeignKey(Customer_Detail, on_delete=models.CASCADE)
	mobile =  models.CharField(max_length=20)
	address = models.TextField(max_length=2000)
	image = models.FileField('Patient Image',upload_to='documents/')
	def __str__(self):
		return self.patient_id
class Report_Detail(models.Model):
	Pid =  models.ForeignKey(Patient_Detail, on_delete=models.CASCADE)
	patient_id =  models.ForeignKey(Customer_Detail, on_delete=models.CASCADE)
	doctor_id =  models.ForeignKey(Doctor_Register, on_delete=models.CASCADE,null=True)
	disease_name =  models.CharField(max_length=200)
	problem =  models.TextField(max_length=200)
	report = models.FileField('Report',upload_to='documents/')
	visiting_date = models.DateField()
	follow_up_date = models.DateField()
	prescription = models.FileField('Prescription',upload_to='documents/')
	def __str__(self):
		return self.patient_id.name
class Disease_Detail(models.Model):
	disease_name =  models.CharField(max_length=200)
	problem =  models.TextField(max_length=2000)
	symtoms =  models.TextField(max_length=2000)
	speed =  models.CharField(max_length=200)
	precautions =  models.TextField(max_length=2000)
	image = models.FileField('Image',upload_to='documents/')
	link =  models.CharField(max_length=2000,null=True)
	date = models.DateField()
	def __str__(self):
		return self.disease_name
class Disease_Category(models.Model):
	name =  models.CharField(max_length=200)
	def __str__(self):
		return self.name
class Disease_Spread(models.Model):
	disease_name =  models.ForeignKey(Disease_Category, on_delete=models.CASCADE)
	area =  models.CharField(max_length=200)
	count =  models.IntegerField('No of Affected Count',null=True)
	cured_count =  models.IntegerField('Cured Count',null=True)
	current_count =  models.IntegerField('No of Currently Affected Count',null=True)
	date = models.DateField()
	def __str__(self):
		return self.disease_name.name
class Disease_Update(models.Model):
	doctor_id =  models.ForeignKey(Doctor_Register, on_delete=models.CASCADE)
	disease_name =  models.ForeignKey(Disease_Category, on_delete=models.CASCADE)
	hospital_name = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	area =  models.CharField(max_length=200)
	count =  models.IntegerField('No of Affected Count',null=True)
	cured_count =  models.IntegerField('Cured Count',null=True)
	current_count =  models.IntegerField('No of Currently Affected Count',null=True)
	def __str__(self):
		return self.hospital_name
class Unauthorised_Disease(models.Model):
	doctor_id =  models.ForeignKey(Doctor_Register, on_delete=models.CASCADE)
	disease_name =  models.CharField(max_length=200)
	problem =  models.TextField(max_length=2000)
	symtoms =  models.TextField(max_length=2000)
	precautions =  models.TextField(max_length=2000)
	date = models.DateField('Posted Date',default=timezone.now())
	def __str__(self):
		return self.disease_name
	def publish(self):
		self.date = timezone.now()
		self.save()


