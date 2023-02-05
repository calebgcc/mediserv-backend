from django.urls import path
from . import views


urlpatterns = [
    path('/experiments', views.get_experiment, name='experiments'),
    path('/experiments/<experiment_id>', views.get_experiment, name='experiment'),
    path('/experiments/add_experiment', views.add_experiment, name='add-experiment'),
]



