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

# Create your views here.

class Eventslist(APIView):
    def get(self, request, format=None):
        today_date = timezone.now().date()
        # curr_time = timezone.now()
        # print(curr_time)
        # print(curr_time + timezone.timedelta(minutes=30),curr_time + timezone.timedelta(minutes=60))
        
        upcevents = Events.objects.filter(date__gt = today_date)

        ongevents = Events.objects.filter(date = today_date)

        ptevents = Events.objects.filter(date__lt = today_date)
        
        upcomingevents = ClubeventsSerializer(upcevents, many = True).data
        ongoingevents = ClubeventsSerializer(ongevents, many = True).data
        pastevents = ClubeventsSerializer(ptevents, many = True).data

        response_data = {
            'upcoming_events' : upcomingevents,
            'ongoing_events' : ongoingevents,
            'past_events' : pastevents,
        }

        return Response(response_data)
    

class Eventsdetails(APIView):
    def get(self, request, clubid, eventid, format=None):
        eventdetails = Events.objects.filter(club_id = clubid , id = eventid).first()
        serializer = EventdetailsSerializer(eventdetails)

        return Response(serializer.data)
    
    def post(self, request, clubid, eventid, format=None):
        print("entered post")
        eventdetails = Events.objects.filter(club_id = clubid , id = eventid).first()
        details = request.data
        teamsize = details['teamsize']
        teamname = details['teamname']
        teammembers = details['teammembers']
        names = [None for i in range(4)]
        rollnos = [None for i in range(4)]
        for i in range(teamsize):
            st = Students.objects.get(roll_no = teammembers[i])
            names[i] = st.name
            rollnos[i] = st
        try:
            registration = Registrations(event_id = eventdetails.id, team_size = teamsize, team_name = teamname, member_1 = names[0], member_1_rollno = rollnos[0], member_2 = names[1], member_2_rollno = rollnos[1] ,member_3 = names[2], member_3_rollno = rollnos[2], member_4 = names[3], member_4_rollno = names[3])
            registration.save()
            
            return Response({'status' : 'success',}, status=status.HTTP_200_OK)
        
        except Exception as e:

            return Response({'status' : str(e),}, status=status.HTTP_400_BAD_REQUEST)

class AdminEventRegistration(APIView):
    def get(self, request, clubid, format=None):
        events = Events.objects.filter(club_id = clubid)
        club = Clubs.objects.get(id = clubid)

        events = EventdetailsSerializer(events, many=True).data
        club = ClubSerializer(club).data

        response = {
            'events' : events,
            'club' : club
        }

        return Response(response)
    
    def post(self, request, clubid, format=None):
        clubid = Clubs.objects.get(id = clubid)
        details = request.data
        eventname = details['eventname']
        min_teamsize = details['min_teamsize']
        max_teamsize = details['max_teamsize']
        date = details['date']
        time = details['time']
        venue = details['venue']
        registrationfee = details['registrationfee']
        prizemoney = details['prizemoney']
        posterurl = details['posterurl']
        description = details['description']
        instructions = details['instructions']

        try:
            event = Events(club_id = clubid, event_name = eventname, poster = posterurl, description= description, instructions = instructions, date = date, time = time, venue = venue, min_team_size = min_teamsize, max_team_size = max_teamsize, registration_fee = registrationfee, prize_money = prizemoney)
            event.save()
            return Response({'status' : 'success',}, status=status.HTTP_200_OK)
        
        except Exception as e:

            return Response({'status' : str(e),}, status=status.HTTP_400_BAD_REQUEST)
        
class AdminEditEvent(APIView):
    def get(self, request, clubid, eventid, format=None):
        club = Clubs.objects.get(id = clubid)
        event = Events.objects.get(id=eventid, club_id = club)

        event = EventdetailsSerializer(event).data
        club = ClubSerializer(club).data

        response = {
            'event' : event,
            'club' : club
        }

        return Response(response)
    
    def put(self, request, clubid, eventid, format=None):
        club = Clubs.objects.get(id = clubid)
        event = Events.objects.get(id=eventid, club_id = club)
        details = request.data
        eventname = details['eventname']
        posterurl = details['posterurl']
        description = details['description']
        instructions = details['instructions']
        date = details['date']
        time = details['time']
        venue = details['venue']
        prizemoney = details['prizemoney']

        try:

            event.event_name = eventname
            event.poster = posterurl
            event.description = description
            event.instructions = instructions
            event.date = date
            event.time = time
            event.venue = venue
            event.prize_money = prizemoney

            event.save()
            return Response({'status' : 'success',}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status' : str(e),}, status=status.HTTP_400_BAD_REQUEST)