from django.db import models

# Create your models here.

from django.db import models
from users.models import *
from clubadmins.models import *
from events.models import *

# Create your models here.

class CustomEventID(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            last_event = model_instance.__class__.objects.order_by('-id').first()
            last_id = int(last_event.id.split('_')[-1]) if last_event else 0
            setattr(model_instance, self.attname, 'etid_' + str(last_id + 1))
        return getattr(model_instance, self.attname)


class Events(models.Model):
    id = CustomEventID(primary_key=True, editable=False, max_length=20)
    club_id = models.ForeignKey('clubadmins.Clubs', on_delete=models.CASCADE, to_field='id')
    event_name = models.CharField(max_length=100, null=False)
    poster = models.URLField(null=False)
    description = models.TextField(null=False)
    instructions = models.TextField(null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    venue = models.CharField(null=False,max_length=500)
    min_team_size = models.IntegerField(null=False)
    max_team_size = models.IntegerField(null=False)
    registration_fee = models.IntegerField(null=False)
    prize_money = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

class CustomRegID(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            last_reg = model_instance.__class__.objects.order_by('-id').first()
            last_id = int(last_reg.id.split('_')[-1]) if last_reg else 0
            setattr(model_instance, self.attname, 'rgid_' + str(last_id + 1))
        return getattr(model_instance, self.attname)

class Registrations(models.Model):
    id = CustomRegID(primary_key=True, editable=False, max_length=20)
    event_id = models.ForeignKey('events.Events', on_delete=models.CASCADE, to_field='id')
    team_size = models.IntegerField(null=False)
    team_name = models.CharField(null=True, max_length=100)
    # team_leader_name = models.CharField(null=False, max_length=100)
    # team_leader_rollno = models.ForeignKey('users.Students', on_delete=models.CASCADE, to_field='roll_no',related_name='team_leader_registration')
    member_1 = models.CharField(null=True, max_length=100)
    member_1_rollno = models.ForeignKey('users.Students', on_delete=models.CASCADE, to_field='roll_no',related_name='member_1_registration')
    member_2 = models.CharField(null=True, max_length=100)
    member_2_rollno = models.ForeignKey('users.Students', on_delete=models.CASCADE, to_field='roll_no',related_name='member_2_registration',null=True)
    member_3 = models.CharField(null=True, max_length=100)
    member_3_rollno = models.ForeignKey('users.Students', on_delete=models.CASCADE, to_field='roll_no',related_name='member_3_registration',null=True)
    member_4 = models.CharField(null=True, max_length=100)
    member_4_rollno = models.ForeignKey('users.Students', on_delete=models.CASCADE, to_field='roll_no',related_name='member_4_registration',null=True)
    