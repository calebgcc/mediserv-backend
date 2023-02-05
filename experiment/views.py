from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Experiment, ExperimentGroup, Participant
from .serializers import ExperimentSerializer, ExperimentGroupSerializer, ParticipantSerializer
import requests
import random


@api_view(['GET'])
def delete_participants(request):
    users = Participant.objects.all()
    for user in users:
        url = f"https://api.tryterra.co/v2/auth/deauthenticateUser?user_id={user.user_id}"

        headers = {
            "accept": "application/json",
            "dev-id": "ichack-dev-v5yHAxTdHW",
            "x-api-key": "56af8f486046727553d9c66335cc0dd4ecad89914438be62ecc976f0c85a963b"
        }

        response = requests.delete(url, headers=headers)
        user.delete()
        user.save()
    return Response({'status':'ok'})


@api_view(['GET'])
def refresh_data(request, experiment_id):
    experiment = Experiment.objects.get(id=experiment_id)
    participants = Participant.objects.filter(experiment=experiment)
    result = {}
    temp = {}
    fakes = 20
    groups = ExperimentGroup.objects.all()
    group_map = {}

    max_group_id = -1
    for group in groups:
        group_map[group.id] = group.name
        max_group_id = max(max_group_id, group.id)

    fake_group_ids = [group_map[random.randint(1, max_group_id)] for _ in range(fakes)]

    for participant in participants:

        url = f"https://api.tryterra.co/v2/daily?user_id={participant.user_id}&start_date=2023-02-01&end_date=2023-02-05&to_webhook=false&with_samples=false"
        print(url)
        headers = {
            "accept": "application/json",
            "dev-id": "ichack-dev-v5yHAxTdHW",
            "x-api-key": "56af8f486046727553d9c66335cc0dd4ecad89914438be62ecc976f0c85a963b"
        }

        response = requests.get(url, headers=headers).json()
        print(response)
        user_id = participant.user_id
        result["name"] = experiment.name
        result["description"] = experiment.description
        result["number_of_groups"] = max_group_id
        temp[user_id] = []
        for day in response['data']:
            temp[user_id].append({
                'avg_oxygen': day['oxygen_data']['avg_saturation_percentage'],
                'steps': day['distance_data']['steps'],
                'avg_heart_rate': day['heart_rate_data']['avg_hr_bpm'],
                'max_heart_rate': day['heart_rate_data']['max_hr_bpm'],
                'calories': day['calories_data']['total_burned_calories'],
                'day': day['metadata']['start_time'],
                'experiment_group_name': group_map[participant.experiment_group],
                'name': participant.name,
            })

            for i in range(fakes):
                fake_user_id = "haksjdfhalkjshalksdjfhvas" + str(i)
                if fake_user_id not in temp:
                    temp[fake_user_id] = []

                temp[fake_user_id].append({
                    'avg_oxygen': random.randint(90, 98),
                    'steps': random.randint(10000, 20000),
                    'avg_heart_rate': random.randint(60, 80),
                    'max_heart_rate': random.randint(80, 120),
                    'calories': random.randint(1500, 2500),
                    'day': day,
                    'experiment_group_name': fake_group_ids[i],
                    'name': "test" + str(i),
                })

    result["users_data"] = temp
    return Response(result)

@api_view(['POST'])
def webhook(request):
    print(request.data)
    if request.data['type'] == 'auth':
        user_id = request.data['user']['user_id']
        experiment, experiment_group, name = request.data['user']['reference_id'].split('-')

        participant = Participant(
            user_id=user_id,
            experiment_id=int(experiment),
            experiment_group_id=int(experiment_group),
            name=name
        )
        participant.save()

    elif request.data['type'] == 'user_reauth':
        old_user_id = request.data['old_user']['user_id']
        old_participant = Participant.objects.filter(user_id=old_user_id)

        experiment = old_participant.experiment_id
        experiment_group = old_participant.experiment_group_id
        name = old_participant.name

        old_participant.delete()
        old_participant.save()

        new_user_id = request.data['new_user']['user_id']
        participant = Participant(
            user_id=new_user_id,
            experiment_id=experiment,
            experiment_group_id=experiment_group,
            name=name
        )
        participant.save()

    elif request.data['type'] == 'deauth':
        old_user_id = request.data['user']['user_id']
        old_participant = Participant.objects.filter(user_id=old_user_id)
        old_participant.delete()
        old_participant.save()
    
    return Response({'status':'ok'})

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
