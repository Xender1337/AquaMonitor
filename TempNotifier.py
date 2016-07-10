# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pushover import Client, init
import os
import django
from django.utils import timezone
import datetime
from decimal import Decimal

# -------------------------------------------------------------------------------------------------------------------- #

# set up django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AquaMonitor.settings")

django.setup()

from IHM.models import Temperature, Probe, Room
msg = ""


def send_msg(msg):
    client = Client("uyxKeBztgT4H5hzjHfiuQhUUnECDHj", api_token="aqzv1irjog4tcp53ove7stsuedxiut", device="motog3renan")
    client.send_message(msg, title="Alert Aqua Temp")

notify = False

for a_room in Room.objects.all():
    for a_probe in Probe.objects.all():
        temp = Temperature.objects.filter(probe=a_probe).latest("datetime").temperature
        print temp
        if a_probe.is_aqua_probe is True and temp >= a_room.max_temp_aqua:
            print a_probe.is_aqua_probe
            print a_room.max_temp_aqua
            notify = True
            msg = "WARNING TEMP REACH\n" + msg
        elif a_probe.is_ext_probe is True and temp >= a_room.max_temp_ext:
            print a_probe.is_ext_probe
            print a_room.max_temp_ext
            notify = True
            msg = "WARNING TEMP REACH\n" + msg
        else:
            print "Nothing to notify"

        msg = a_probe.label + "\n" + str(temp) + "°C \n" + msg

    if notify:
        send_msg(msg)
