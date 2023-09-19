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
            return HttpResponse("""
            <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Conference Rooms</title>
                </head>
                <body>
                    <!-- Nav -->
                    <h1>Conference Rooms Navigation Menu</h1>
                    <nav>
                        <a href="http://127.0.0.1:8000/all_rooms/">Show all conference rooms</a>
                        <a href="/room/new/">Add new conference room</a>
                    </nav>
                    <!-- Nav -->
                        <h2>There are no conference rooms yet</h2>
                    <!-- Footer -->
                    <footer>
                        <p>Author: Jakub Mierzyński</p>
                        <p><a href="mailto:jakub.mierzynski@gmail.com">jakub.mierzynski@gmail.com</a></p>
                    </footer>
                    <!-- Footer -->
                
                </body>
                </html>
            """)

        table = HttpResponse("""
                <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>All conference rooms</title>
        </head>
        <body>
                    <!-- Nav -->
            <h1>Conference Rooms Navigation Menu</h1>
            <nav>
                <a href="http://127.0.0.1:8000/all_rooms/">Show all conference rooms</a><br>
                <a href="/room/new/">Add new conference room</a><br><br>
            </nav>
            <!-- Nav -->
            <!-- Table -->
            <table border=solid black 1px>
                <tr>
                    <th>Name of room</th>
                    <th>Capacity</th>
                    <th>Available</th>
                    <th>Projector available</th>
                    <th>Edit room</th>
                    <th>Delete room</th>
                    <th>Reserve room</th>
                </tr>
        """)

        for room in all_rooms:
            table.write(f"""
            <tr>
                <td><a href="http://127.0.0.1:8000/room/{room.pk}">{room.room_name}</a></td>
                <td>{room.room_capacity}</td>
                <td>{room.room_available}</td>
                <td>{room.projector_available}</td>
                <td><a href="http://127.0.0.1:8000/modify/{room.pk}">PRESS TO EDIT ROOM</a></td>
                <td><a href="http://127.0.0.1:8000/delete/{room.pk}">PRESS TO DELETE ROOM</a></td>
                <td><a href="http://127.0.0.1:8000/reserve/{room.pk}">PRESS TO RESERVE ROOM</a></td>
            </tr>
            """)

        table.write("""
            </table>
            <footer>
                <p>Author: Jakub Mierzyński</p>
                <p><a href="mailto:jakub.mierzynski@gmail.com">jakub.mierzynski@gmail.com</a></p>
            </footer>
            <!-- Table -->
            <!-- Footer -->
        </body>
        </html>
        """)

        return table


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
        date_to_check = datetime.date(int(splitted_reservation_date[0]),
                                      int(splitted_reservation_date[1]),
                                      int(splitted_reservation_date[2]))

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

        # reservation_date = request.POST.get("date")
        # room_id = int(room_id)
        # # Creating datetime from reservation date to compare later with today's date
        # split_reservation_date = reservation_date.split("-")
        # date_to_check = datetime.date(int(split_reservation_date[0]),
        #                               int(split_reservation_date[1]),
        #                               int(split_reservation_date[2]))
        #
        # room_id = request.POST.get("room_id")
        #
        # if date_to_check < datetime.date.today():
        #     return HttpResponse("Room cannot be reserved for a day from past")
        #
        # all_reservations = RoomReservation.objects.all()
        #
        # for reservation in all_reservations:
        #     if reservation.room_id.pk == room_id and reservation.date == date_to_check:
        #         return HttpResponse()
        #
        # return HttpResponse("TEST")












