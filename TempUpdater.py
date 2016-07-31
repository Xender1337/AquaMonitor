#!/usr/bin/env python

import subprocess
import re
import os
import django
import time
from django.utils import timezone
import datetime
import calendar
import redis

# -------------------------------------------------------------------------------------------------------------------- #

# set up django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AquaMonitor.settings")

django.setup()

print datetime.datetime.now()
from IHM.models import Temperature, Probe

r = redis.StrictRedis(host='localhost', port=0, db=0, unix_socket_path="/tmp/redis.sock")
first_start = True

while True:
    if first_start is True:
        print "Flush old data"
        r.flushall()

        print "load data from DB"
        for a_probe in Probe.objects.all():
            for a_value in Temperature.objects.filter(probe=a_probe).order_by("datetime"):
                timestamp = calendar.timegm(a_value.datetime.timetuple()) * 1000
                r.rpush(a_probe.name, str(timestamp) + ", " + str(float(a_value.temperature)))

        first_start = False

    print("Sleep for 150 sec.")
    time.sleep(150)

    base_dir = '/sys/bus/w1/devices/'
    probes = os.listdir(base_dir)
    print datetime.datetime.now()
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

            r.rpush(probe.name, str(calendar.timegm(datetime.datetime.now().timetuple()) * 1000) + ", " + str(float(temp)))
            r.rpush("last_update", str(datetime.datetime.now()))

        else:
            print "Not a probe"

