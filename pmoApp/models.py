from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.core.validators import *
from django.contrib.auth.models import User

# Create your models here.
class CMOPlanReport(models.Model):
	planID = models.IntegerField(primary_key=True)
	caseID = models.IntegerField()
	crisisName = models.CharField(max_length=250)
	emergencyLevel = models.CharField(max_length=250)
	crisisDescription = models.CharField(max_length=100000)
	planDescription = models.CharField(max_length=100000)
	crsisDateTime = models.DateTimeField()
	
	def __str__(self):
		return str(self.caseID)
		
class authorizationReport(models.Model): #only by PM
	authorizationID = models.IntegerField(primary_key=True)
	planID = models.ForeignKey(CMOPlanReport, on_delete=models.CASCADE, null=False)
	dateTime = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.authorizationID)
		
class justificationReport(models.Model): #only by PM
	justificationID = models.IntegerField(primary_key=True)
	planID = models.ForeignKey(CMOPlanReport, on_delete=models.CASCADE, null=False)
	justification = models.CharField(max_length=100000, null=False)
	dateTime = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.justificationID)

class statusReport(models.Model):
	statRepID = models.IntegerField(primary_key=True)
	caseID = models.ForeignKey(CMOPlanReport, on_delete=models.CASCADE, null=False)
	crisisStatus = models.CharField(max_length=250) #Open (create ourselves), Ongoing, Closed
	dateTime = models.DateTimeField(auto_now_add=True)
	locationDispatched = models.CharField(max_length=250)
	latitude = models.FloatField()
	longitude = models.FloatField()
	areaAffected = models.CharField(max_length=250)
	statusDescription = models.CharField(max_length=100000,null=True,)
	
	def __str__(self):
		return str(self.statRepID)

class Account(models.Model):
	username = models.CharField(max_length=15, primary_key=True)
	handphone_number = models.IntegerField(
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(80000000)
        ]
    )
	user_type = models.CharField(max_length=15)  #Enum: PM, DPM, DM, HM, IM, TM
	minister_name = models.CharField(max_length=500)
	profilePicURL = models.CharField(max_length=150, null=True, blank=True)
	profilePicture = models.ImageField(upload_to='profilepics', blank=True)
	decisionTable = models.ImageField(upload_to='decisiontables', blank=True)
	def __str__(self):
		return self.user_type

class Plan_Evaluation(models.Model): #Comments by All Ministers except PM
	Plan_Evaluation_id = models.IntegerField(primary_key=True)
	planID = models.ForeignKey(CMOPlanReport, on_delete=models.CASCADE, null=False)
	user_type = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
	authorizationStatus = models.CharField(max_length=500, null=True, blank=True) #Approved, Pending, Rejected
	eval_dateTime = models.DateTimeField(auto_now_add=True)
	eval_comment = models.CharField(max_length=500, null=True, blank=True)
	eval_hasComment = models.BooleanField(default=False)
	

class Post(models.Model):
    title= models.CharField(max_length=300, unique=True)
    content= models.TextField()