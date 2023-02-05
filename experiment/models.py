from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    date_created = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Test Parameters
    heart_rate_avg = models.BooleanField(default=False)
    heart_rate_max = models.BooleanField(default=False)
    blood_pressure = models.BooleanField(default=False)
    blood_glucose = models.BooleanField(default=False)
    steps = models.BooleanField(default=False)
    oxygen_data = models.BooleanField(default=False)
    burned_calories = models.BooleanField(default=False)


class ExperimentGroup(models.Model):
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Participant(models.Model):
    name = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    experiment_group = models.ForeignKey(ExperimentGroup, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=300)
