from django.shortcuts import render, HttpResponse
from IHM.models import Temperature, Probe
import subprocess
from django.http import JsonResponse
import calendar
from django.utils import timezone
import redis
import datetime
import time

timezone.localtime(timezone.now())


def index(request):
    r = redis.StrictRedis(host='localhost', port=6379, db=0, unix_socket_path="/tmp/redis.sock")
    probe_temp = {}
    probe_color = ["#aaeeee", "#90ee7e", "#2b908f"]
    last_update = r.rpop("last_update")
    r.rpush("last_update", last_update)

    for a_probe in Probe.objects.all():
        min = r.rpop("min_temp." + a_probe.name)
        max = r.rpop("max_temp." + a_probe.name)
        cur = r.rpop("cur_temp." + a_probe.name)
        probe_temp[a_probe.label + "  (today)"] = {"Current ": cur, "Max": max, "Min": min}

    print "Temp max/min probes"
    print probe_temp

    return render(request, "index.html", {
        "probe_temps": probe_temp,
        "probe_color": probe_color,
        "last_update": last_update[:-7],
    })


def settings(request):
    base_dir = '/sys/bus/w1/devices/'
    p = subprocess.Popen(["ls", base_dir], stdout=subprocess.PIPE)
    probes = p.stdout.readlines()
    result = []

    for a_probe in probes:
        print a_probe[3:-1]
        if a_probe[3:-1].isalnum():
            result.append(a_probe)
    print result
    return render(request, 'settings.html', {'probes': result,})


def get_json(request):
    index = 1
    count = 0
    data = {}
    start = datetime.datetime.now()
    r = redis.StrictRedis(host='localhost', port=6379, db=0, unix_socket_path="/tmp/redis.sock")

    for a_probe in Probe.objects.all():
        max_temp = None
        min_temp = None
        curent_temp = None
        data['data' + str(index)] = []
        result = r.lrange(a_probe.name, 0, -1)
        print(datetime.datetime.now() - start)

        current_month = datetime.datetime.now().month
        cureent_day = datetime.datetime.now().day

        for a_line in result:
            line = a_line.strip()
            fields = line.split(',')

            date = datetime.datetime.fromtimestamp(int(fields[0][:-3])).timetuple()
            if date.tm_mday == cureent_day and date.tm_mon == current_month:
                temp_float = float(fields[1])
                if max_temp is None:
                    max_temp = temp_float
                elif max_temp < temp_float:
                    max_temp = temp_float

                if min_temp is None:
                    min_temp = temp_float
                elif min_temp > temp_float:
                    min_temp = temp_float

                curent_temp = temp_float
            data['data' + str(index)].append([int(fields[0]), float(fields[1])])
            count += 1
        data['data' + str(a_probe.name)] = ([max_temp, min_temp])
        r.rpush("min_temp." + a_probe.name, min_temp)
        r.rpush("max_temp." + a_probe.name, max_temp)
        r.rpush("cur_temp." + a_probe.name, curent_temp)
        print(datetime.datetime.now() - start)
        index += 1
    data['value_nbr'] = str(count)
    return JsonResponse(data)
