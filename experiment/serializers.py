from rest_framework import serializers
from .models import Experiment, ExperimentGroup, Participant

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'

class ExperimentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentGroup
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'



