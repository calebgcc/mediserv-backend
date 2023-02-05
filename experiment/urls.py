from django.urls import path
from . import views


urlpatterns = [
    path('experiments/', views.get_experiments, name='experiments'),
    path('experiments/add_experiment/', views.add_experiment, name='add-experiment'),
    path('experiments/add_group/', views.add_experiment_group, name='add-experiment-group'),
    path('experiments/add_participant/', views.add_participant, name="add-participant"),
    path('experiments/<experiment_id>/', views.refresh_data, name='experiment'),
    path('data/', views.webhook, name='webhook'),
    path('delete/', views.delete_participants, name='delete')
    # path('experiments/<experiment_id>/refresh_data', views.refresh_data, name='refresh_data')
]



