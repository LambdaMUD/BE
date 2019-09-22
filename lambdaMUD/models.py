from django.db import models
import uuid


class Room(models.Model):
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    wall_n = models.BooleanField(default=True)
    wall_s = models.BooleanField(default=True)
    wall_e = models.BooleanField(default=True)
    wall_w = models.BooleanField(default=True)

    def knock_down_wall(self, other, wall):
        """When building maze: Knock down the wall between rooms self and other."""
        # A wall separates a pair of cells in the N-S or W-E directions.
        wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        if wall == 'N':
            self.wall_n = False
            other.wall_s = False
        elif wall == 'S':
            self.wall_s = False
            other.wall_n = False
        elif wall == 'E':
            self.wall_e = False
            other.wall_w = False
        elif wall == 'W':
            self.wall_w = False
            other.wall_e = False
        self.save()
        other.save()
    
    def has_all_walls(self):
        if self.wall_n and self.wall_s and self.wall_e == True and self.wall_w == True:
            return True
        else:
            return False
