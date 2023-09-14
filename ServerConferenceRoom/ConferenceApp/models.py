from django.db import models


# Create your models here.
class ConferenceRoomModel(models.Model):
    room_name = models.CharField(max_length=225, unique=True)
    room_capacity = models.IntegerField(null=False)
    projector_available = models.BooleanField(null=False)


