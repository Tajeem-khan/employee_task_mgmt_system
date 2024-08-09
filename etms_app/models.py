from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
 
class Employee(models.Model):
    name = models.CharField(max_length=65)
    phone = models.IntegerField()
    address = models.TextField()
    dob = models.DateField()
    doj = models.DateField()
    user =models.OneToOneField(User, null=True, on_delete=models.SET_NULL )

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    deadline = models.DateTimeField()
    attachments =models.ImageField(blank=True,null=True,)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    doa = models.DateTimeField(auto_now_add=True)  # date of assign
    doc = models.DateTimeField(blank=True,null=True)  #date of completion
    
    
    def __str__(self):
        return self.title  + ". Assigned to:" + self.employee.name
     