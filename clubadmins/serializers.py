from rest_framework import serializers

from users.models import *
from clubadmins.models import *
from events.models import *

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clubs
        fields = ("id","name","logo","aboutus","vision","mission","insta_link","homephoto")
        
class ClubeventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ("id","club_id","event_name","poster","description")

class CoreCommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreCommittee
        fields = ("club_id","president","vice_president","treasurer")

class ClubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = ("id","club_id","name","email")