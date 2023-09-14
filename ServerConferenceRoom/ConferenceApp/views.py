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
        # if method is get, return form for new conference room
        # form = HttpResponse("""
        # <form action="" method="POST">
        #     <label for="room_name">Room name:</label><br>
        #     <input type="text" name="room_name" id="room_name"><br>
        #     <label for="room_capacity">Room capacity:</label><br>
        #     <input type="number" name="room_capacity" id="room_capacity" min=1><br>
        #     <label for="projector_available">Projector available</label><br>
        #     <input type="checkbox" id="projector_available" name="projector_available" value="True"><br><br>
        #     <input type="submit" value="Submit">
        # </form>
        # """)
        #
        # return form
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

        return HttpResponseRedirect("http://127.0.0.1:8000/")






