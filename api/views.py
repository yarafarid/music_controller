from django.shortcuts import render
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import (
    Response,
)  # this is a class that allows us to send a custom JSON response from the API
from django.http import JsonResponse


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"  # this is the name of the url parameter that we are going to use to get the room code

    def get(self, request, format=None):
        code = request.GET.get(
            self.lookup_url_kwarg
        )  # .GET is giving information about URL FROM THE GET REQUEST
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:  # check if the room exists
                data = RoomSerializer(room[0]).data
                data["is_host"] = (
                    self.request.session.session_key == room[0].host
                )  # make a new key in the data dictionary called is_host and set it to true if the session key is equal to the host of the room
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"Room Not Found": "Invalid Room Code."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"Bad Request": "Code parameter not found in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer  # It tells the view which serializer to use for handling the incoming data.

    def post(
        self, request, format=None
    ):  # this is a method that will be called when the user clicks the create room button it will take the data from the request and make sure that's all the data is valid
        if request.method == "POST":  # check if the request is a POST request
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            serializer = self.serializer_class(
                data=request.data
            )  # take the data from the request and make sure that's all the data is valid
            if serializer.is_valid():
                guest_can_pause = serializer.data.get("guest_can_pause")
                votes_to_skip = serializer.data.get("votes_to_skip")
                host = self.request.session.session_key
                queryset = Room.objects.filter(host=host)
                if (
                    queryset.exists()
                ):  # check if the host already has a room if so update the room with the new values
                    room = queryset[
                        0
                    ]  # in this line we are getting the first room that the host has created
                    room.guest_can_pause = guest_can_pause
                    room.votes_to_skip = votes_to_skip
                    room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                    self.request.session["room_code"] = room.code
                    return Response(
                        RoomSerializer(room).data, status=status.HTTP_200_OK
                    )
                else:
                    room = Room(
                        host=host,
                        guest_can_pause=guest_can_pause,
                        votes_to_skip=votes_to_skip,
                    )
                    room.save()
                    self.request.session["room_code"] = room.code
                    return Response(
                        RoomSerializer(room).data, status=status.HTTP_201_CREATED
                    )
            return Response(
                {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
            )


class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get(
            self.lookup_url_kwarg
        )  # .data is a dictionary that contains the data that was sent in the  POST request
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session["room_code"] = (
                    room.code  # make a new key in the session dictionary called room_code and set it to the code of the room, to indicate this user in this current session is in this room, to be used in user_in_room view
                )
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)
            return Response(
                {"Bad Request": "Invalid Room Code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"Bad Request": "Invalid post data, did not find a code key"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {"code": self.request.session.get("room_code")}
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request):
        if "room_code" in self.request.session:
            self.request.session.pop(
                "room_code"
            )  # remove the room code from the user session
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            code = serializer.data.get("code")
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response(
                    {"msg": "Room not found"}, status=status.HTTP_404_NOT_FOUND
                )
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response(
                    {"msg": "You are not the host of this room"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        return Response(
            {"Bad Request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST
        )
