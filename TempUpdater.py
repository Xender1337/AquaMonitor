#!/usr/bin/env python

import subprocess
import re
import os
import django
import time
from django.utils import timezone
import datetime

# -------------------------------------------------------------------------------------------------------------------- #

# set up django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AquaMonitor.settings")

django.setup()

print datetime.datetime.now()
from IHM.models import Temperature, Probe, Room

while True:
    base_dir = '/sys/bus/w1/devices/'
    probes = os.listdir(base_dir)
    print probes

    for a_probe in probes:
        print a_probe
        if a_probe[3:].isalnum():
            path = base_dir + a_probe + "/w1_slave"

            p = open(path, 'r')
            result = p.readlines()
            m = re.search('(?<=t=)\w+', result[1])
            print float(m.group(0)) / 1000
            temp = float(m.group(0)) / 1000

            print ""
            probe = Probe.objects.filter(name=a_probe).get()

            temperature = Temperature(temperature=temp, probe=probe, datetime=datetime.datetime.now())
            temperature.save()

        else:
            print "Not a probe"

    time.sleep(60)