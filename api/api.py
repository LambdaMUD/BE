from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from lambdaMUD.models import Room
from django.http import JsonResponse
from django.http import HttpResponse
import json
import random


# ***************************************************************
class Maze:
    """A Maze, represented as a grid of rooms."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """
        Initialize the maze grid.
        The maze consists of nx * ny rooms and will be constructed starting
        at the room indexed at (ix, iy).
        """
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        Room.objects.all().delete()
        self.maze_map = [[Room(row=x, column=y) for y in range(ny)] for x in range(nx)]
        for x in range(self.nx):
            for y in range(self.ny):
                self.maze_map[x][y].save()

    def room_at(self, x, y):
        """Return the Room object at (x,y)."""

        return self.maze_map[x][y]

    def find_valid_neighbours(self, room):
        """Return a list of unvisited neighbours to room."""

        delta = [('W', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in delta:
            x2, y2 = room.row + dx, room.column + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.room_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours
    
    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx*2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].wall_e:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].wall_s:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def make_maze(self):
        # Total number of rooms.
        n = self.nx * self.ny
        room_stack = []
        current_room = self.room_at(self.ix, self.iy)
        # Total number of visited rooms during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_room)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_room = room_stack.pop()
                continue

            # Choose a random neighboring room and move to it.
            direction, next_room = random.choice(neighbours)
            current_room.knock_down_wall(next_room, direction)
            room_stack.append(current_room)
            current_room = next_room
            nv += 1
    
    def toList(self):
        """Return a list representation of the maze."""
        maze = []

        for y in range(self.ny):
            for x in range(self.nx):
                room = {
                    'row': y, 
                    'column': x, 
                    'wall_n': self.maze_map[x][y].wall_n, 
                    'wall_s': self.maze_map[x][y].wall_s, 
                    'wall_e': self.maze_map[x][y].wall_e, 
                    'wall_w': self.maze_map[x][y].wall_w
                }
                maze.append(room)
        return maze

# ***************************************************************


@csrf_exempt
@api_view(["POST"])
def make_maze(request):
    data = json.loads(request.body)
    rows = data['rows']
    columns = data['columns']
    maze = Maze(rows, columns)
    maze.make_maze()
    print(maze)
    return JsonResponse({'rows': rows, 'columns': columns, 'maze': maze.toList()})
