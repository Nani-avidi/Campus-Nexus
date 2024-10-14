from django.contrib import admin
from users.models import *
from clubadmins.models import *
from events.models import *

# Register your models here.

admin.site.register(Events)
admin.site.register(Registrations)