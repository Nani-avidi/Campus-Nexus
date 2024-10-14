from rest_framework import serializers

from users.models import *
from clubadmins.models import *
from events.models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ("roll_no","name","email")

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class StEventRegSerializer(serializers.ModelSerializer):
    event = EventsSerializer(source='event_id')

    class Meta:
        model = Registrations
        fields = '__all__'
