from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    date_created = models.DateField(auto_now_add=True)
    num_of_groups = models.IntegerField()
    num_of_samples = models.IntegerField()
    
