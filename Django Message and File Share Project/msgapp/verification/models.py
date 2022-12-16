from django.db import models

# Create your models here.

class App_Users(models.Model):
    mobile = models.CharField(null= False, primary_key= True, max_length=10)
    name = models.CharField(null = False, max_length=20)
    counter = models.IntegerField(default = 0, null = True)