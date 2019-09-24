from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from .models import *


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    if request.user.player:
        player = request.user.player
    else:
        player = Player(user=user)
        player.save()
    player_id = player.id
    uuid = player.uuid
    current_room = player.current_room()
    return JsonResponse({'uuid': uuid, 'name': player.user.username}, safe=True)


@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    current_room = player.current_room()
    nextRoom = None
    if direction == "n":
        # going up one row
        nextRoom = (current_room[0]+1, current_room[1])
    elif direction == "s":
        # going down one row
        nextRoom = (current_room[0]-1, current_room[1])
    elif direction == "e":
        # move forward one column
        nextRoom = (current_room[0], current_room[1]+1)
    elif direction == "w":
        # move back one column
        nextRoom = (current_room[0], current_room[1]-1)
    if nextRoom[0] >= 0 and nextRoom[1] >= 0:
        player.row = nextRoom[0]
        player.column = nextRoom[1]
        player.save()
        return JsonResponse(
            {
                'name': player.user.username,
                'row': player.row,
                'column': player.column,
                'error_msg': ""
            }, safe=True)
    else:
        return JsonResponse(
            {
                'name': player.user.username,
                'error_msg': "You cannot move that way."
            }, safe=True)
