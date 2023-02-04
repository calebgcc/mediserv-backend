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
