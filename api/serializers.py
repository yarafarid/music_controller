# We need to create endpoint that can return to us information about the rooms in a format that we can use in our frontend like JSON.
# The serializer will take our model ROOM and convert it into JSON format response.
from rest_framework import serializers
from .models import Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')


 # serialize the request  "take data from the request" and make sure that's all the data is valid  
 # and then keep it to us in a kind of python format that we can use in our views.
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')
class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[]) # in this line we are creating a new field called code and we are setting it to a charField and we are passing in a list of validators that we want to use to validate the code
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code') # we are adding the code field that we created to be part of the fields that we want to serialize