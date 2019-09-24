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
    print(f"current room: n: {current_room.wall_n}, s:{current_room.wall_s}, e: {current_room.wall_e}, w: {current_room.wall_w}")
    return JsonResponse(
        {
            'uuid': uuid,
            'name': player.user.username,
            'row': current_room.row,
            'column': current_room.column,
        }, safe=True)


@csrf_exempt
@api_view(["GET"])
def reset(request):
    user = request.user
    if request.user.player:
        player = request.user.player
    else:
        player = Player(user=user)
        player.save()
    player_id = player.id
    uuid = player.uuid
    player.reset()
    current_room = player.current_room()
    print(f"current room: n: {current_room.wall_n}, s:{current_room.wall_s}, e: {current_room.wall_e}, w: {current_room.wall_w}")
    return JsonResponse(
        {
            'uuid': uuid,
            'name': player.user.username,
            'row': current_room.row,
            'column': current_room.column,
        }, safe=True)

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
    nextRoom_coordinates = (-1, -1)
    if direction == "n":
        # going up one row
        if not current_room.wall_n:
            nextRoom_coordinates = (current_room.row+1, current_room.column)
    elif direction == "s":
        # going down one row
        if not current_room.wall_s:
            nextRoom_coordinates = (current_room.row-1, current_room.column)
    elif direction == "e":
        # move forward one column
        if not current_room.wall_e:
            nextRoom_coordinates = (current_room.row, current_room.column+1)
    elif direction == "w":
        # move back one column
        if not current_room.wall_w:
            nextRoom_coordinates = (current_room.row, current_room.column-1)
    try:
        next_room = Room.objects.get(row=nextRoom_coordinates[0], column=nextRoom_coordinates[1])
        player.currentRoom = next_room.id
        player.save()
        print(f"current room: n: {next_room.wall_n}, s:{next_room.wall_s}, e: {next_room.wall_e}, w: {next_room.wall_w}")
        return JsonResponse(
            {
                'name': player.user.username,
                'row': next_room.row,
                'column': next_room.column,
                'error_msg': ""
            }, safe=True)
    except Room.DoesNotExist:
        return JsonResponse(
            {
                'name': player.user.username,
                'error_msg': "You cannot move that way."
            }, safe=True)
