from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Room(models.Model):
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    wall_n = models.BooleanField(default=True)
    wall_s = models.BooleanField(default=True)
    wall_e = models.BooleanField(default=True)
    wall_w = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
        if self.wall_n and self.wall_s and self.wall_e and self.wall_w:
            return True
        else:
            return False

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.all()]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.filter(user=self.user).first().id
            self.save()

    def reset(self):
        self.currentRoom = Room.objects.filter(user=self.user).first().id
        self.save()

    def current_room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.current_room()


# Create a Player as soon as a User is saved
@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


#  Save the Player to the database
@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
