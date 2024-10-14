from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import *
from clubadmins.models import *
from events.models import *

from users.serializers import *
from clubadmins.serializers import *
from events.serializers import *

from django.utils import timezone
from django.db.models import Q

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class Clubslist(APIView):
    def get(self, request, format=None):
        c = Clubs.objects.all()
        serializer = ClubSerializer(c, many = True)
        return Response(serializer.data)
    
class Clubevents(APIView):
    def get(self, request, clubid, format=None):
        club = Clubs.objects.get(id=clubid)
        today_date = timezone.now().date()
        # curr_time = timezone.now()
        # print(curr_time)
        # print(curr_time + timezone.timedelta(minutes=30),curr_time + timezone.timedelta(minutes=60))
        
        upcevents = Events.objects.filter(date__gt = today_date , club_id = clubid)

        ongevents = Events.objects.filter(date = today_date , club_id = clubid)

        ptevents = Events.objects.filter(date__lt = today_date , club_id = clubid)
        
        upcomingevents = ClubeventsSerializer(upcevents, many = True).data
        ongoingevents = ClubeventsSerializer(ongevents, many = True).data
        pastevents = ClubeventsSerializer(ptevents, many = True).data

        club = ClubSerializer(club).data

        response_data = {
            'upcoming_events' : upcomingevents,
            'ongoing_events' : ongoingevents,
            'past_events' : pastevents,
            'club' : club
        }

        return Response(response_data)
    
class Clubinfo(APIView):
    def get(self, request, clubid, format=None):
        club = Clubs.objects.get(id = clubid)
        corecommittee = CoreCommittee.objects.get(club_id = clubid)

        corecommitteeserializer = CoreCommitteeSerializer(corecommittee).data
        clubserializer = ClubSerializer(club).data

        response = {
            'club' : clubserializer,
            'corecommittee' : corecommitteeserializer
        }

        return Response(response)
    
class ClubAdminsRegister(APIView):
    def get(self, request, format=None):
        admins = Admins.objects.all()
        clubs = Clubs.objects.all()

        adminsserializer = ClubAdminSerializer(admins, many=True).data
        clubserializer = ClubSerializer(clubs,many=True).data

        response = {
            'admins' : adminsserializer,
            'clubs' : clubserializer
        }

        return Response(response)
    
    def post(self, request, format=None):
        details = request.data
        name = details.get('name')
        club_id = details.get('club_id')
        email = details.get('email')
        password = details.get('password')
        clubid = Clubs.objects.get(id=club_id)

        admin = Admins(name=name, club_id=clubid, email=email)
        admin.set_password(password)
        admin.save()

        return Response({'status':'success'},status=status.HTTP_200_OK)
    
class ClubAdminLogin(APIView):
    def get(self, request, format=None):
        admins = Admins.objects.all()
        clubs = Clubs.objects.all()

        adminsserializer = ClubAdminSerializer(admins, many=True).data
        clubserializer = ClubSerializer(clubs,many=True).data

        response = {
            'admins' : adminsserializer,
            'clubs' : clubserializer
        }

        return Response(response)
    
    def post(self, request, format=None):
        details = request.data
        email = details['email']
        club_id = details['club_id']
        password = details['password']
        club_id = Clubs.objects.get(id=club_id)

        admin = Admins.objects.get(email = email, club_id = club_id)

        if admin.check_password(password):
                    refresh = RefreshToken.for_user(admin)
                    print("correct password")
                    return Response({'status':'success',
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),}, status=status.HTTP_200_OK)
        else:
            print("wrong password")
            return Response({'status':'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)

    
    