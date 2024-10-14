from rest_framework import serializers

from users.models import *
from clubadmins.models import *
from events.models import *

from clubadmins.serializers import *


class EventdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ("id","club_id","event_name","poster","description","instructions","date","time","venue","min_team_size","max_team_size","registration_fee","prize_money")

class EventRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrations
        fields = ("id","event_id","team_size","team_name","member_1","member_1_rollno","member_2","member_2_rollno","member_3","member_3_rollno","member_4","member_4_rollno")
