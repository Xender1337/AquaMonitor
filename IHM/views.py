from django.shortcuts import render, HttpResponse
from IHM.models import Temperature, Probe
import subprocess
import json
from django.http import JsonResponse
import calendar
from django.utils import timezone
timezone.localtime(timezone.now())

def index(request):
    return render(request, "index.html", {})


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

    data = {}
    #result = {"pointInterval": 60000}
    #result["pointStart"] = calendar.timegm(Temperature.objects.earliest("datetime").datetime.timetuple()) * 1000 + 7200000
    #result["date"] = Temperature.objects.earliest("datetime").datetime
    for a_probe in Probe.objects.all():
        data['data' + str(index)] = []
        for a_value in Temperature.objects.filter(probe=a_probe).order_by("datetime"):
            data['data' + str(index)].append([calendar.timegm(a_value.datetime.timetuple()) * 1000 + 7200000, float(a_value.temperature)])
            #data['data' + str(index)].append(float(a_value.temperature))
        index += 1
    #result["dataLength"] = count
    return JsonResponse(data)
