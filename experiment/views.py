from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Experiment, ExperimentGroup, Participant
from .serializers import ExperimentSerializer, ExperimentGroupSerializer, ParticipantSerializer
import requests


@api_view(['POST'])
def webhook(request):
    if 'auth' in request.data:
        user_id = request.data['user']['user_id']
        experiment, experiment_group, name = request.data['user']['reference_id'].split('-')

        participant = Participant(
            user_id=user_id,
            experiment=experiment,
            experiment_group=experiment_group,
            name=name
        )
        participant.save()
    elif 'user_reauth' in request.data:
        old_user_id = request.data['old_user']['user_id']
        old_participant = Participant.object.filter(user_id=old_user_id)

        experiment = old_participant.experiment
        experiment_group = old_participant.experiment_group
        name = old_participant.name

        old_participant.delete()

        new_user_id = request.data['new_user']['user_id']
        participant = Participant(
            user_id=new_user_id,
            experiment=experiment,
            experiment_group=experiment_group,
            name=name
        )
        participant.save()

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
        **experiment_serializer.data,
        'groups': groups_serializer.data,
        'participants': particpants_serializer.data,
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

    except Exception as e:
        print("Error adding experiment: ", e)
        return Response({'status':False})

@api_view(['POST'])
def add_experiment_group(request):
    
    try:
        experiment_group = ExperimentGroup(
            name=request.data['name'],
            experiment_id=request.data['experiment'],)
        experiment_group.save()

        response = {
            'status': True,
            'experiment_group_id': experiment_group.id,
        }
        return Response(response)

    except Exception as e:
        print(e)
        return Response({'status':False})

@api_view(['POST'])
def add_participant(request):

    try:
        url = "https://api.tryterra.co/v2/auth/generateWidgetSession"

        payload = {
            "reference_id": str(request.data['experiment'])+"-"+str(request.data['experiment_group'])+"-"+request.data['name'],
            "providers": "GARMIN,WITHINGS,FITBIT,GOOGLE,OURA,WAHOO,PELOTON,ZWIFT,TRAININGPEAKS,FREESTYLELIBRE,DEXCOM,COROS,HUAWEI,OMRON,RENPHO,POLAR,SUUNTO,EIGHT,APPLE,CONCEPT2,WHOOP,IFIT,TEMPO,CRONOMETER,FATSECRET,NUTRACHECK,UNDERARMOUR",
            "language": "en"
        }
        headers = {
            "accept": "application/json",
            "dev-id": "ichack-dev-v5yHAxTdHW",
            "content-type": "application/json",
            "x-api-key": "56af8f486046727553d9c66335cc0dd4ecad89914438be62ecc976f0c85a963b"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return Response({'status':True,'link':response.json()["url"]})

    except Exception as e:
        print(e)
        return Response({'status':False})


def get_exp(experiment):

    experiment_serializer = ExperimentSerializer(experiment, many=False)

    groups = ExperimentGroup.objects.filter(experiment=experiment)
    participants = Participant.objects.filter(experiment=experiment)

    experiment = {
        **experiment_serializer.data,
        'num_groups': len(groups),
        'num_participants': len(participants),
    } 

    return experiment
