from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ConferenceApp.models import ConferenceRoomModel, RoomReservation
import datetime


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class AddNewConferenceRoom(View):
    def get(self, request):
        return TemplateResponse(request, "adding_room_form.html")

    def post(self, request):
        # if method is post create variables:
        new_room_name = request.POST.get("room_name")
        new_room_capacity = request.POST.get("room_capacity")
        print(new_room_name)
        print(new_room_capacity)

        is_projector_available = True if request.POST.get("projector_available") == "True" else False
        print(is_projector_available)

        # import all rooms, to check if room with such name doesn't already exist
        all_rooms = ConferenceRoomModel.objects.all()

        # Validation is room name isn't None and if Room with such a name doesn't already exist
        if new_room_name is None:
            return HttpResponse("Please fill name for conference room.")
        else:
            for room in all_rooms:
                if room.room_name == new_room_name:
                    return HttpResponse(f"Conference room with {new_room_name} already exists")

        # Validation if room capacity isn't None or <= 0
        if new_room_capacity is None:
            return HttpResponse("Please fill capacity for conference room")
        else:
            if int(new_room_capacity) <= 0:
                return HttpResponse("Conference room capacity cannot be 0 or lower")

        # Creating new ConferenceRoomModel
        new_conference_room = ConferenceRoomModel.objects.create(
            room_name=new_room_name,
            room_capacity=int(new_room_capacity),
            projector_available=is_projector_available
        )

        new_conference_room.save()

        return HttpResponseRedirect("http://127.0.0.1:8000/all_rooms/")


@method_decorator(csrf_exempt, name="dispatch" )
class AllAvailableRooms(View):
    def get(self, request):
        all_rooms = ConferenceRoomModel.objects.all()

        if len(all_rooms) == 0:
            return render(request, "table_all_rooms.html", context={"error": "No rooms available"})

        for room in all_rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates

        return render(request, "table_all_rooms.html", context={"all_rooms": all_rooms})


@method_decorator(csrf_exempt, name="dispatch")
class DeleteRoom(View):
    def get(self, request, room_id):
        room_id = int(room_id)

        ConferenceRoomModel.objects.filter(pk=room_id).delete()

        return HttpResponseRedirect("http://127.0.0.1:8000/all_rooms/")


@method_decorator(csrf_exempt, name="dispatch")
class ModifyRoom(View):
    def get(self, request, room_id):
        # Creating template form html form.
        room = ConferenceRoomModel.objects.get(pk=int(room_id))

        temp = {
            "room_name": room.room_name,
            "room_capacity": room.room_capacity,
            "room_id": int(room_id),
            "projector_available": room.projector_available
        }

        return render(request, "edit_room.html", temp)

    def post(self, request, room_id):
        all_rooms = ConferenceRoomModel.objects.all()
        new_capacity = request.POST.get("capacity")
        new_name = request.POST.get("room_name")
        is_projector_available = True if request.POST.get("projector_available") == "True" else False
        room_id = request.POST.get("room_id")

        # Validation of capacity value
        if len(new_capacity) == 0:
            return HttpResponse("Please fill capacity")
        try:
            new_capacity = int(new_capacity)
        except ValueError:
            return HttpResponse("Capacity cannot be other than number")


        # Validation of new name. We are allowing to change only capacity or all specifications
        if len(new_name) == 0:
            return HttpResponse("Please fill room name")
        for room in all_rooms:
            if room.room_name == new_name:
                if int(room.pk) == int(room_id):
                    pass
                else:
                    return HttpResponse("Room name is already occupied. Try other one")

        # Editing and saving changes in conference room
        edited_room = ConferenceRoomModel.objects.get(pk=room_id)
        edited_room.room_name = new_name
        edited_room.room_capacity = new_capacity
        edited_room.projector_available = is_projector_available
        edited_room.save()

        return HttpResponseRedirect("http://127.0.0.1:8000/all_rooms/")



@method_decorator(csrf_exempt, name="dispatch")
class ReserveRoomClass(View):
    def get(self, request, room_id):
        room = ConferenceRoomModel.objects.get(pk=int(room_id))
        return render(request, "reserve_room.html", context={"room": room})

    def post(self, request, room_id):
        room = ConferenceRoomModel.objects.get(pk=int(room_id))
        reservation_date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        splitted_reservation_date = reservation_date.split("-")

        try:
            date_to_check = datetime.date(int(splitted_reservation_date[0]),
                                          int(splitted_reservation_date[1]),
                                          int(splitted_reservation_date[2]))
        except ValueError:
            return render(request,
                          "reserve_room.html",
                          context={"room": room, "error": "Fill reservation date"})

        # Check if room isn't already booked for that day
        if RoomReservation.objects.filter(date=reservation_date, room=room):
            return render(request,
                          "reserve_room.html",
                          context={"room": room, "error": "Room already booked for that day"})

        # Check if date of reservation isn't from past
        if date_to_check < datetime.date.today():
            return render(request,
                          "reserve_room.html",
                          context={"error": "Reservation date is from the past"})

        # Make reservation and redirect to all rooms view
        RoomReservation.objects.create(date=reservation_date, room=room, comment=comment)
        return HttpResponseRedirect("http://127.0.0.1:8000/all_rooms")


@method_decorator(csrf_exempt, name="dispatch")
class ShowSpecification(View):
    def get(self, request, room_id):
        room = ConferenceRoomModel.objects.get(pk=room_id)
        reservations = room.roomreservation_set.filter(date__gte=(datetime.date.today())).order_by("date")

        return render(request, "room_specification.html", context={"room": room, "reservations": reservations})













