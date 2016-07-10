from django.shortcuts import render
from IHM.models import Temperature
import subprocess


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
