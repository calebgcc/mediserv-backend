from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    date_created = models.DateField(auto_now_add=True)

class ExperimentGroup(models.Model):
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Participant(models.Model):
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    experiment_group = models.ForeignKey(ExperimentGroup, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=300)






