from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from pusher import Pusher
from decouple import config

from .models import *

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

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
    players = current_room.playerNames(player_id)
    return JsonResponse(
        {
            'uuid': uuid,
            'name': player.user.username,
            'row': current_room.row,
            'column': current_room.column,
            'players': players
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
    players = current_room.playerNames(player_id)
    return JsonResponse(
        {
            'uuid': uuid,
            'name': player.user.username,
            'row': current_room.row,
            'column': current_room.column,
            'players': players
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
            nextRoom_coordinates = (current_room.row-1, current_room.column)
    elif direction == "s":
        # going down one row
        if not current_room.wall_s:
            nextRoom_coordinates = (current_room.row+1, current_room.column)
    elif direction == "e":
        # move forward one column
        if not current_room.wall_e:
            nextRoom_coordinates = (current_room.row, current_room.column+1)
    elif direction == "w":
        # move back one column
        if not current_room.wall_w:
            nextRoom_coordinates = (current_room.row, current_room.column-1)
    try:
        next_room = Room.objects.get(row=nextRoom_coordinates[0], column=nextRoom_coordinates[1], user=request.user)
        player.currentRoom = next_room.id
        player.save()
        players = next_room.playerNames(player_id)
        return JsonResponse(
            {
                'name': player.user.username,
                'row': next_room.row,
                'column': next_room.column,
                'players': players,
                'error_msg': ""
            }, safe=True)
    except Room.DoesNotExist:
        players = current_room.playerNames(player_id)
        return JsonResponse(
            {
                'name': player.user.username,
                'row': current_room.row,
                'column': current_room.column,
                'players': players,
                'error_msg': "You cannot move that way."
            }, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    data = json.loads(request.body)
    message = data['message']
    pusher.trigger(
        f'lambda-mud-channel',
        u'broadcast',
        {'message': f'Player {player.user.username}: {message}'}
    )
    return JsonResponse({'message': f"The message {message} was sent"}, safe=True)