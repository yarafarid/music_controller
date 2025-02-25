# store URLs local to this app
from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom
urlpatterns = [
    path('', RoomView.as_view()), # when the user goes to the root URL "Blank URL", the main view will be called
    path('room', RoomView.as_view()), 
    path('create-room', CreateRoomView.as_view()), 
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view()),
]
