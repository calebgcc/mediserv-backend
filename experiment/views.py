from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Experiment, ExperimentGroup, Participant
from .serializers import ExperimentSerializer, ExperimentGroupSerializer, ParticipantSerializer

@api_view(['GET'])
def get_experiments(request):
    experiments = Experiment.objects.all()

    response = []
    for experiment in experiments:
        experiment = get_exp(experiment)
        response.append(experiment)

    return Response(response)

@api_view(['GET'])
def get_experiment(request, experiment_id):
    experiment = Experiment.objects.get(id=experiment_id)
    experiment_serializer = ExperimentSerializer(experiment, many=False)

    groups = ExperimentGroup.objects.filter(experiment=experiment)
    groups_serializer = ExperimentGroupSerializer(groups, many=True)

    particpants = Participant.objects.filter(experiment=experiment)
    particpants_serializer = ParticipantSerializer(particpants, many=True)
    
    experiment = {
        **experiment_serializer,
        'groups': groups_serializer,
        'participants': particpants_serializer,
    }

    return Response(experiment)

@api_view(['POST'])
def add_experiment(request):

    try:
        experiment = Experiment(
            name=request.data['name'], 
            description=request.data['description'],)
        experiment.save()

        response = {
            'status': True,
            'experiment_id': experiment.id,
        }
        return Response(response)

    except:
        return Response({'status':False})

@api_view(['POST'])
def add_experiment_group(request):
    
    try:
        experiment_group = ExperimentGroup(
            name=request.data['name'],
            experiment=request.data['experiment'],)
        experiment_group.save()

        response = {
            'status': True,
            'experiment_group_id': experiment_group.id,
        }
        return Response(response)

    except:
        return Response({'status':False})

@api_view(['POST'])
def add_participant(request):

    try:
        participant = Participant(
            name=request.data['name'],
            experiment=request.data['experiment'],
            experiment_group=request.data['experiment_group'],
            user_id=request.data['user_id'],)
        participant.save()

        response = {
            'status': True,
            'participant_id': participant.id,
        }
        return Response(response)
    except:
        return Response({'status':False})


def get_exp(experiment):

    experiment_serializer = ExperimentSerializer(experiment, many=False)

    groups = ExperimentGroup.objects.count(experiment=experiment)
    participants = Participant.objects.count(experiment=experiment)

    experiment = {
        **experiment_serializer,
        'num_groups': groups,
        'num_participants': participants,
    } 

    return experiment

