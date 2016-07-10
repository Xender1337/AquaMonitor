from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    max_temp_ext = models.DecimalField(decimal_places=3, blank=True, max_digits=6)
    max_temp_aqua = models.DecimalField(decimal_places=3, blank=True, max_digits=6)

    def __unicode__(self):
        return self.name


class Probe(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    label = models.CharField(max_length=255, blank=True, unique=False)
    room = models.ForeignKey(Room)
    last_update = models.DateTimeField(auto_now=True)
    is_aqua_probe = models.BooleanField(default=False)
    is_ext_probe = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Temperature(models.Model):
    temperature = models.DecimalField(decimal_places=3, blank=False, max_digits=6)
    datetime = models.DateTimeField(auto_now_add=True)
    probe = models.ForeignKey(Probe)

    def __unicode__(self):
        return str(self.temperature)
