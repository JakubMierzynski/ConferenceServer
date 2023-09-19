from django.db import models



class ConferenceRoomModel(models.Model):
    room_name = models.CharField(max_length=225, unique=True)
    room_capacity = models.IntegerField(null=False)
    room_available = models.BooleanField(default=True)
    projector_available = models.BooleanField(null=False)


class RoomReservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(ConferenceRoomModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)


    class Meta:
        unique_together = ("room", "date")

