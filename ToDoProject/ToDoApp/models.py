from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Step(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks')
    file = models.FileField(upload_to='uploads/', blank=True)
    status = models.CharField(max_length=10, default='to do')
    important = models.CharField(max_length=15, default='no important')
    date = models.DateField('date')
    note = models.TextField(max_length=150, default='')  
    steps = models.ManyToManyField(Step)  
    

    def __str__(self) -> str:
        return self.name


