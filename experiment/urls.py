from django.urls import path
from . import views


urlpatterns = [
    path('experiments/', views.get_experiments, name='experiments'),
    path('experiments/add_experiment/', views.add_experiment, name='add-experiment'),
    path('experiments/<experiment_id>/', views.get_experiment, name='experiment'),
]



