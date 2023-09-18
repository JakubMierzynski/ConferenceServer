from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ConferenceApp.models import ConferenceRoomModel


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
                <a href="http://127.0.0.1:8000/all_rooms/">Show all conference rooms</a>
                <a href="/room/new/">Add new conference room</a>
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








