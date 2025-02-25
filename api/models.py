from django.db import models
import string
import random
def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length)) # generate a random string of length 6 only with uppercase letters
        if Room.objects.filter(code=code).count() == 0:
            break

    return code
# Group similar users together in a room thar room will have control over the host music
# oner user will be the host and the rest will be the guests and they can control the music
class Room(models.Model):
    code = models.CharField(max_length=8, unique=True, default=generate_unique_code) # unique code for the room
    host = models.CharField(max_length=50, unique=True) #one host can only have one room
    guest_can_pause = models.BooleanField(null=False, default=False) # null =false means that we must pass a value
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True) # when the room is created