from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class CustomClubID(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            last_club = model_instance.__class__.objects.order_by('-id').first()
            last_id = int(last_club.id.split('_')[-1]) if last_club else 0
            setattr(model_instance, self.attname, 'clid_' + str(last_id + 1))
        return getattr(model_instance, self.attname)

class Clubs(models.Model):
    id = CustomClubID(primary_key=True,editable=False,max_length=20)
    name = models.CharField(null=False,max_length = 100)
    logo = models.URLField(null=False)
    aboutus = models.TextField(null=False)
    vision = models.TextField(null=False)
    mission = models.TextField(null=False)
    insta_link = models.URLField(null=False)
    homephoto = models.URLField(null=False)
    
    class Meta:
        ordering = ('name',)


class CustomAdminID(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            last_admin = model_instance.__class__.objects.order_by('-id').first()
            last_id = int(last_admin.id.split('_')[-1]) if last_admin else 0
            setattr(model_instance, self.attname, 'adid_' + str(last_id + 1))
        return getattr(model_instance, self.attname)

class Admins(models.Model):
    id = CustomAdminID(primary_key=True,editable=False,max_length=20)
    club_id = models.ForeignKey(Clubs, on_delete=models.CASCADE, to_field='id')
    name = models.CharField(null=False,max_length = 100)
    email = models.EmailField(max_length=254, unique=True, null = False)
    password = models.CharField(max_length=128, null=False)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class CoreCommittee(models.Model):
    club_id = models.ForeignKey(Clubs, on_delete=models.CASCADE, to_field='id')
    president = models.CharField(null=False,max_length = 100)
    vice_president = models.CharField(null=False,max_length = 100)
    treasurer = models.CharField(null=False,max_length = 100)
