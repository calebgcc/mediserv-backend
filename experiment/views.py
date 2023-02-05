from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Experiment
from .serializers import ExperimentSerializer

@api_view(['GET'])
def get_experiments(request):
    experiments = Experiment.objects.all()
    serializer = ExperimentSerializer(experiments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_experiment(request, experiment_id):
    experiment = Experiment.objects.get(id=experiment_id)
    serializer = ExperimentSerializer(experiment, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def add_experiment(request):
    experiment = Experiment(
        name=request.data['name'], 
        description=request.data['description'], 
        num_of_groups=request.data['num_of_groups'], 
        num_of_participants=request.data['num_of_participants'])
    experiment.save()
    return Response({'status':True})


