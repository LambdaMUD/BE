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

        self[f"wall_{wall}"] = False
        other[f"wall_{wall_pairs[wall]}"] = False
