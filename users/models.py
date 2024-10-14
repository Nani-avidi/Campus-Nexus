from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from users.models import *
from clubadmins.models import *
from events.models import *


# Create your models here.

class Students(models.Model):
    roll_no = models.CharField(primary_key = True, max_length = 15)
    name = models.CharField(null=False,max_length = 100)
    email = models.EmailField(max_length=254, unique=True, null = False)
    password = models.CharField(max_length=128, null=False)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.roll_no