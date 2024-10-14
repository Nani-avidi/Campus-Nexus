from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import *
from clubadmins.models import *
from events.models import *

from clubadmins.serializers import *
from events.serializers import *
from users.serializers import *

from django.utils import timezone
from django.db.models import Q

from rest_framework_simplejwt.tokens import RefreshToken


class StRegValidation(APIView):
    def get(self, request, clubid, eventid, format=None):
        st = Students.objects.all()
        reg = Registrations.objects.filter(event_id=eventid)
        et = Events.objects.get(id = eventid)

        students = StudentSerializer(st, many = True).data
        registrations = EventRegistrationsSerializer(reg, many = True).data
        event = EventdetailsSerializer(et).data

        response_data = {
            'Students' : students,
            'Registrations' : registrations,
            'Event' : event
        }

        return Response(response_data)
    
    def post(self, request, clubid, eventid, format=None):
        print("entered post")
        eventdetails = Events.objects.filter(club_id = clubid , id = eventid).first()
        details = request.data
        teamsize = details['teamsize']
        teamname = details['teamname']
        teammembers = details['teammembers']
        names = [None for i in range(4)]
        rollnos = [None for i in range(4)]
        print(eventdetails)
        for i in range(teamsize):
            st = Students.objects.get(roll_no = teammembers[i])
            names[i] = st.name
            rollnos[i] = st
        print(names,rollnos)
        try:
            registration = Registrations(event_id = eventdetails, team_size = teamsize, team_name = teamname, member_1 = names[0], member_1_rollno = rollnos[0], member_2 = names[1], member_2_rollno = rollnos[1] ,member_3 = names[2], member_3_rollno = rollnos[2], member_4 = names[3], member_4_rollno = names[3])
            registration.save()
            
            return Response({'status' : 'success',}, status=status.HTTP_200_OK)
        
        except Exception as e:

            return Response({'status' : str(e),}, status=status.HTTP_400_BAD_REQUEST)
    
class Stregistrations(APIView):
    def get(self, request, strollno, format=None):
        strollno = strollno.upper()
        reg = Registrations.objects.filter(Q(member_1_rollno = strollno) | Q(member_2_rollno = strollno) | Q(member_3_rollno = strollno) | Q(member_4_rollno = strollno)).select_related('event_id')

        myregserializer = StEventRegSerializer(reg, many=True)
        
        return Response(myregserializer.data)
        
class StudentRegistration(APIView):
    def get(self, request, fromat=None):
        st = Students.objects.all()
        students = StudentSerializer(st, many = True)

        return Response(students.data)
    
    def post(self, request, format=None):
        details = request.data
        name = details.get('name')
        roll_no = details.get('rollNo')
        email = details.get('email')
        password = details.get('password')

        student = Students(name=name, roll_no=roll_no, email=email)
        student.set_password(password)
        student.save()

        return Response({'status':'success'},status=status.HTTP_200_OK)
    
class StudentLogin(APIView):
    def get(self, request, format=None):
        st = Students.objects.all()
        students = StudentSerializer(st, many = True)

        return Response(students.data)
    
    def post(self, request, format=None):
        details = request.data
        roll_no = details.get('rollNo')
        password = details.get('password')
        student = Students.objects.get(roll_no = roll_no)

        if student.check_password(password):
            refresh = RefreshToken.for_user(student)
            print("correct password")
            return Response({'status':'success',
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),}, status=status.HTTP_200_OK)
        else:
            print("wrong password")
            return Response({'status':'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)