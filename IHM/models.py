from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)


class Probe(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    room = models.ForeignKey(Room)
    last_update = models.DateTimeField(auto_now=True)


class Temperature(models.Model):
    temperature = models.DecimalField(decimal_places=2, blank=False, max_digits=6)
    datetime = models.DateTimeField(auto_now_add=True)
    probe = models.ForeignKey(Probe)
