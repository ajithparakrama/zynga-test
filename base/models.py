from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

class User(AbstractUser):
    user_type = models.BooleanField(default=False)
    avatar = models.ImageField(null=True,default='avatar.svg')
    history = HistoricalRecords()
    email = models.EmailField(unique=True)



class Plan_Type(models.Model):
    name = models.CharField(max_length=200)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
   
class Functional_area(models.Model):
    name=models.CharField(max_length=30)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    
    
class Investment_priority(models.Model):
    name=models.CharField(max_length=30)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    

class Assets_Type(models.Model):
    name=models.CharField(max_length=30)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    
    
class Capex_Type(models.Model):
    name=models.CharField(max_length=30)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    
    
class Expected_Servince(models.Model):
    name=models.CharField(max_length=30)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    
    
class Status(models.Model):
    name=models.CharField(max_length=20)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name    

class Approve_Status(models.Model):
    name=models.CharField(max_length=20)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
class record(models.Model):
    record_id   = models.CharField(max_length=20,null=True) 
    company_code   = models.CharField(max_length=20,null=True) 
    functional_area =  models.ForeignKey(Functional_area, on_delete=models.SET_NULL,null=True)
    cost_center = models.CharField(max_length=50,null=True)
    plan_type = models.ForeignKey(Plan_Type, on_delete=models.SET_NULL,null=True)
    year = models.CharField(max_length=4,null=True)
    investment_priority = models.ForeignKey(Investment_priority, on_delete=models.SET_NULL,null=True)
    assets_type = models.ForeignKey(Assets_Type, on_delete=models.SET_NULL,null=True)
    capex_type = models.ForeignKey(Capex_Type, on_delete=models.SET_NULL,null=True)
    preview_number = models.CharField(max_length=20,null=True)
    asset_to_be_replace = models.CharField(max_length=20,null=True)
    expected_inverstment_value = models.DecimalField(decimal_places=3, max_digits=15,null=True)
    expected_servince_category = models.ForeignKey(Expected_Servince,on_delete=models.SET_NULL,null=True)
    expected_savings_value = models.CharField(max_length=20,null=True)
    project_start_date = models.DateField(null=True)
    project_end_date = models.DateField(null=True)
    status = models.ForeignKey(Status,on_delete=models.SET_NULL,null=True)    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ) 
    approve_time = models.DateTimeField(null=True)  
    approve_status = models.ForeignKey(Approve_Status, on_delete=models.SET_NULL, null=True)
    confirmation = models.BooleanField(default=False,null=False)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-updated','-created']
        
    def __str__(self):
        return self.record_id

    