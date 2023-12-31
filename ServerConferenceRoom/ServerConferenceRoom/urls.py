"""
URL configuration for ServerConferenceRoom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from ConferenceApp.views import AddNewConferenceRoom, AllAvailableRooms, DeleteRoom, ModifyRoom, ReserveRoomClass,\
    ShowSpecification, SearchRoom, MainPage

urlpatterns = [
    path("", MainPage.as_view()),
    path("admin/", admin.site.urls),
    path("room/new/", AddNewConferenceRoom.as_view()),
    path("all_rooms/", AllAvailableRooms.as_view()),
    path("search-room/", SearchRoom.as_view()),
    re_path(r"^delete/(?P<room_id>\d+)/$", DeleteRoom.as_view()),
    re_path(r"^modify/(?P<room_id>\d+)/$", ModifyRoom.as_view()),
    re_path(r"^reserve/(?P<room_id>\d+)/$", ReserveRoomClass.as_view()),
    re_path(r"^show-specification/(?P<room_id>\d+)/$", ShowSpecification.as_view()),
]
